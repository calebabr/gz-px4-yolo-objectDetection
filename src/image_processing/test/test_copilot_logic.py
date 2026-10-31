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
    assert seen['messages'][0]['content'] == logic.PERSONAS['friendly_guide']


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
