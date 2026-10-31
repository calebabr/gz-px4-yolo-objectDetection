"""Pure helpers for the copilot bridge. No ROS imports, so they can be unit tested anywhere."""
import base64
import json
import urllib.error
import urllib.request

DEFAULT_MODEL = 'gpt-4o-mini'
API_URL = 'https://api.openai.com/v1/chat/completions'

PERSONAS = {
    'default': (
        'You are the on-board copilot of a search drone. Answer in one or two short sentences. '
        'Use only the game state, the detections and the camera image provided. '
        'If something is not in them, say you do not know. Never invent targets.'),
    'friendly_guide': (
        'You are a cheerful guide helping a child on a treasure hunt with a drone. '
        'Use simple words and at most two short sentences. '
        'Only talk about what is in the provided state, detections and image. '
        'If you are not sure, say so kindly. Never invent treasure.'),
}


# T1 = brief, T2 = standard, T3 = full (set by Unity from the AI condition; T0 never calls the copilot).
DETAIL_INSTRUCTIONS = {
    'brief': 'Keep it to one short sentence. Give only the recommendation: no numbers and no reasoning.',
    'standard': 'Answer in one or two sentences. Include a distance or a confidence only when it helps.',
    'full': ('Answer in up to four sentences. Explain your reasoning, say how confident the detections are '
             'and what you are unsure about.'),
}


class CopilotError(Exception):
    """Raised when the language-model call fails. The message is safe to show to the player."""


def persona_prompt(persona_id):
    return PERSONAS.get(persona_id or 'default', PERSONAS['default'])


def detail_instruction(detail):
    return DETAIL_INSTRUCTIONS.get(detail or 'standard', DETAIL_INSTRUCTIONS['standard'])


def summarize_detections(detections):
    """detections: list of dicts with class_name, confidence (0..1) and optionally distance (m)."""
    if not detections:
        return 'no detections right now'
    parts = []
    for d in detections[:10]:
        text = '%s (%.0f%%)' % (d.get('class_name', '?'), 100.0 * float(d.get('confidence', 0.0)))
        if 'distance' in d:
            text += ' about %.0f m away' % float(d['distance'])
        parts.append(text)
    return ', '.join(parts)


def build_messages(question, persona_id, state, detections, image_jpeg=None, detail='standard'):
    """Chat-completion messages: persona + detail level as system prompt, grounded context + question (+ camera frame) as user."""
    context = 'Game state: %s\nDetections: %s' % (
        json.dumps(state or {}, sort_keys=True), summarize_detections(detections))
    content = [{'type': 'text', 'text': context + '\nPlayer question: ' + question}]
    if image_jpeg:
        encoded = base64.b64encode(image_jpeg).decode('ascii')
        content.append({'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + encoded}})
    return [
        {'role': 'system', 'content': persona_prompt(persona_id) + ' ' + detail_instruction(detail)},
        {'role': 'user', 'content': content},
    ]


def mock_answer(question, state, detections, detail='standard'):
    """Deterministic stand-in used for tests and offline demos. Grounded in the same inputs as the real call."""
    state = state or {}
    found = state.get('found', '?')
    total = state.get('total', '?')
    if detail == 'brief':
        names = sorted({d.get('class_name', '?') for d in (detections or [])})
        return 'Mock copilot: I see %s.' % (', '.join(names) if names else 'nothing yet')

    answer = 'Mock copilot: I see %s.' % summarize_detections(detections)
    answer += ' You have found %s of %s' % (found, total)
    if 'timeRemaining' in state:
        answer += ' with %d seconds left' % int(float(state['timeRemaining']))
    answer += '.'
    if detail == 'full':
        answer += (' Reasoning: these come from the camera frame and the YOLO detector; '
                   'anything under 40% confidence deserves a second look.')
    return answer


def call_openai(messages, api_key, model=DEFAULT_MODEL, timeout=20.0, url=API_URL):
    """One chat-completion request using only the standard library. Never logs the key or the response body."""
    body = json.dumps({
        'model': model,
        'messages': messages,
        'max_tokens': 120,
        'temperature': 0.2,
    }).encode('utf-8')
    request = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key,
    })
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        raise CopilotError('the language model returned HTTP %d' % error.code)
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise CopilotError('could not reach the language model (%s)' % getattr(error, 'reason', error))
    except ValueError:
        raise CopilotError('the language model sent an unreadable reply')

    try:
        return payload['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError, TypeError, AttributeError):
        raise CopilotError('the language model sent an unexpected reply')


def answer_question(question, persona_id, state, detections, image_jpeg, api_key, model,
                    mock=False, timeout=20.0, caller=call_openai, detail='standard'):
    """Returns (text, source) where source is 'mock', 'offline', 'openai' or 'error'."""
    if mock:
        return mock_answer(question, state, detections, detail), 'mock'
    if not api_key:
        return 'Copilot offline: no OpenAI key is set on the ROS machine.', 'offline'
    try:
        messages = build_messages(question, persona_id, state, detections, image_jpeg, detail)
        return caller(messages, api_key, model, timeout), 'openai'
    except CopilotError as error:
        return 'Copilot error: %s' % error, 'error'
