import json
import urllib.error

import pytest

from image_processing import copilot_logic as logic


STATE = {'found': 2, 'total': 8, 'timeRemaining': 120.7}
DETECTIONS = [{'class_name': 'person', 'confidence': 0.91, 'distance': 12.4}]


def test_summarize_detections_empty_and_populated():
    assert logic.summarize_detections([]) == 'no detections right now'
    text = logic.summarize_detections(DETECTIONS)
    assert 'person (91%)' in text and '12 m' in text


def test_summarize_detections_limits_to_ten():
    many = [{'class_name': 'c%d' % i, 'confidence': 0.5} for i in range(25)]
    assert logic.summarize_detections(many).count('%') == 10


def test_build_messages_text_only():
    messages = logic.build_messages('Where are they?', 'default', STATE, DETECTIONS)
    assert [m['role'] for m in messages] == ['system', 'user']
    parts = messages[1]['content']
    assert len(parts) == 1 and parts[0]['type'] == 'text'
    assert 'Where are they?' in parts[0]['text']
    assert '"found": 2' in parts[0]['text'] and 'person (91%)' in parts[0]['text']


def test_build_messages_with_image_is_base64_data_url():
    messages = logic.build_messages('hi', 'default', STATE, [], image_jpeg=b'\xff\xd8abc')
    image = messages[1]['content'][1]
    assert image['type'] == 'image_url'
    assert image['image_url']['url'].startswith('data:image/jpeg;base64,')


def test_persona_selected_and_unknown_falls_back():
    assert 'child' in logic.persona_prompt('friendly_guide')
    assert logic.persona_prompt('does_not_exist') == logic.PERSONAS['default']
    assert logic.persona_prompt(None) == logic.PERSONAS['default']


def test_mock_answer_is_deterministic_and_grounded():
    first = logic.mock_answer('q', STATE, DETECTIONS)
    assert first == logic.mock_answer('q', STATE, DETECTIONS)
    assert 'person' in first and '2 of 8' in first and '120 seconds' in first


def test_answer_question_mock_never_calls_the_model():
    def boom(*args, **kwargs):
        raise AssertionError('must not be called')
    text, source = logic.answer_question('q', 'default', STATE, DETECTIONS, None, 'key', 'm', mock=True, caller=boom)
    assert source == 'mock' and text.startswith('Mock copilot')


def test_answer_question_without_key_is_offline_not_an_exception():
    text, source = logic.answer_question('q', 'default', STATE, DETECTIONS, None, '', 'm')
    assert source == 'offline' and 'offline' in text


def test_answer_question_uses_injected_caller_and_passes_messages():
    seen = {}

    def fake(messages, api_key, model, timeout):
        seen.update(messages=messages, key=api_key, model=model, timeout=timeout)
        return 'I see one person.'

    text, source = logic.answer_question('q', 'friendly_guide', STATE, DETECTIONS, b'jpg', 'k', 'gpt-test', caller=fake)
    assert (text, source) == ('I see one person.', 'openai')
    assert seen['key'] == 'k' and seen['model'] == 'gpt-test'
    assert seen['messages'][0]['content'].startswith(logic.PERSONAS['friendly_guide'])


def test_answer_question_turns_model_errors_into_a_player_message():
    def fail(*args, **kwargs):
        raise logic.CopilotError('network down')
    text, source = logic.answer_question('q', 'default', STATE, DETECTIONS, None, 'k', 'm', caller=fail)
    assert source == 'error' and 'network down' in text


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_call_openai_parses_reply_and_sends_bearer_header(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured['auth'] = request.get_header('Authorization')
        captured['body'] = json.loads(request.data.decode('utf-8'))
        return _Response({'choices': [{'message': {'content': '  Two people ahead.  '}}]})

    monkeypatch.setattr(logic.urllib.request, 'urlopen', fake_urlopen)
    reply = logic.call_openai([{'role': 'user', 'content': 'x'}], 'secret', model='gpt-test')
    assert reply == 'Two people ahead.'
    assert captured['auth'] == 'Bearer secret'
    assert captured['body']['model'] == 'gpt-test' and captured['body']['max_tokens'] == 120


def test_call_openai_http_error_does_not_leak_key_or_body(monkeypatch):
    def fake_urlopen(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 401, 'Unauthorized', {}, None)

    monkeypatch.setattr(logic.urllib.request, 'urlopen', fake_urlopen)
    with pytest.raises(logic.CopilotError) as error:
        logic.call_openai([], 'sk-very-secret')
    assert '401' in str(error.value) and 'sk-very-secret' not in str(error.value)


def test_call_openai_network_error_and_bad_reply(monkeypatch):
    def unreachable(request, timeout):
        raise urllib.error.URLError('offline')

    monkeypatch.setattr(logic.urllib.request, 'urlopen', unreachable)
    with pytest.raises(logic.CopilotError):
        logic.call_openai([], 'k')

    monkeypatch.setattr(logic.urllib.request, 'urlopen', lambda request, timeout: _Response({'nope': 1}))
    with pytest.raises(logic.CopilotError):
        logic.call_openai([], 'k')


# ---- explanation detail (T1 brief / T2 standard / T3 full) ----

def test_detail_instruction_per_level_and_unknown_falls_back_to_standard():
    assert 'no numbers' in logic.detail_instruction('brief')
    assert 'reasoning' in logic.detail_instruction('full')
    assert logic.detail_instruction('standard') == logic.DETAIL_INSTRUCTIONS['standard']
    assert logic.detail_instruction('nonsense') == logic.DETAIL_INSTRUCTIONS['standard']
    assert logic.detail_instruction(None) == logic.DETAIL_INSTRUCTIONS['standard']


def test_system_prompt_combines_persona_and_detail():
    brief = logic.build_messages('q', 'default', STATE, DETECTIONS, detail='brief')[0]['content']
    full = logic.build_messages('q', 'default', STATE, DETECTIONS, detail='full')[0]['content']
    assert brief.startswith(logic.PERSONAS['default']) and 'no numbers' in brief
    assert full.startswith(logic.PERSONAS['default']) and 'reasoning' in full
    assert brief != full


def test_mock_answer_brief_has_class_names_but_no_confidence_or_counts():
    text = logic.mock_answer('q', STATE, DETECTIONS, detail='brief')
    assert 'person' in text and '%' not in text and 'of 8' not in text


def test_mock_answer_standard_is_unchanged_and_full_adds_reasoning():
    standard = logic.mock_answer('q', STATE, DETECTIONS)
    assert standard == logic.mock_answer('q', STATE, DETECTIONS, detail='standard')
    assert '2 of 8' in standard and 'Reasoning' not in standard
    full = logic.mock_answer('q', STATE, DETECTIONS, detail='full')
    assert full.startswith(standard) and 'Reasoning' in full and '40%' in full


def test_mock_answer_brief_with_no_detections():
    assert 'nothing yet' in logic.mock_answer('q', STATE, [], detail='brief')


def test_answer_question_passes_the_detail_through():
    seen = {}

    def fake(messages, api_key, model, timeout):
        seen['system'] = messages[0]['content']
        return 'ok'

    logic.answer_question('q', 'default', STATE, DETECTIONS, None, 'k', 'm', caller=fake, detail='full')
    assert 'reasoning' in seen['system']
    text, source = logic.answer_question('q', 'default', STATE, DETECTIONS, None, '', 'm', mock=True, detail='brief')
    assert source == 'mock' and '%' not in text
