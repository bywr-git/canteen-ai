from unittest.mock import Mock

import pytest
import requests

from app.config import settings
from app.services import food_vision


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self.payload = payload or {}
        self.headers = {'Content-Type': 'application/json'}

    def json(self):
        return self.payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(response=self)


def valid_response(text='{"food_name":"Dosa","serving_size":"1 serving","calories":300,"protein_g":8,"confidence":0.8,"notes":"Estimate"}'):
    return FakeResponse(200, {"candidates": [{"content": {"parts": [{"text": text}]}}]})


def test_success_constructs_configured_rest_request(monkeypatch):
    captured = {}

    def post(url, **kwargs):
        captured.update(url=url, kwargs=kwargs)
        return valid_response()

    monkeypatch.setattr(food_vision.requests, 'post', post)
    monkeypatch.setattr(settings, 'GEMINI_API_KEY', 'test-secret')
    monkeypatch.setattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash')

    result = food_vision.analyze_image(b'fake-image', 'image/jpeg')

    assert captured['url'] == 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'
    assert captured['kwargs']['params'] == {'key': 'test-secret'}
    assert captured['kwargs']['timeout'] == 30
    request = captured['kwargs']['json']
    image_part = request['contents'][0]['parts'][0]['inline_data']
    assert image_part['mime_type'] == 'image/jpeg'
    assert image_part['data'] == 'ZmFrZS1pbWFnZQ=='
    assert request['contents'][0]['parts'][1]['text'] == food_vision.ANALYSIS_PROMPT
    assert request['generationConfig']['responseMimeType'] == 'application/json'
    assert 'tools' not in request
    assert result['food_name'] == 'Dosa'
    assert result['estimated_calories'] == 300


def test_http_diagnostics_are_safe_and_include_status(caplog, monkeypatch):
    response = FakeResponse(404, {'error': {'status': 'NOT_FOUND', 'message': 'model unavailable'}})
    monkeypatch.setattr(food_vision.requests, 'post', lambda *args, **kwargs: response)
    monkeypatch.setattr(settings, 'GEMINI_API_KEY', 'secret-not-logged')
    monkeypatch.setattr(settings, 'GEMINI_MODEL', 'gemini-3.6-flash')

    with caplog.at_level('INFO', logger='app.services.food_vision'):
        with pytest.raises(food_vision.FoodVisionError):
            food_vision.analyze_image(b'image', 'image/jpeg')

    logs = caplog.text
    assert 'GEMINI_REQUEST_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent' in logs
    assert 'GEMINI_HTTP_STATUS=404' in logs
    assert 'GEMINI_CONTENT_TYPE=application/json' in logs
    assert 'GEMINI_ERROR_TYPE=NOT_FOUND' in logs
    assert 'GEMINI_ERROR_MESSAGE=model unavailable' in logs
    assert 'secret-not-logged' not in logs


def test_structured_response_is_parsed():
    response = valid_response('{"food_name":"Rice","serving_size":"one bowl","calories":250,"protein_g":6,"carbohydrates_g":48,"fat_g":2,"fiber_g":3,"confidence":0.6,"notes":"Estimate"}')
    mock_post = Mock(return_value=response)
    original = food_vision.requests.post
    food_vision.requests.post = mock_post
    original_key = settings.GEMINI_API_KEY
    settings.GEMINI_API_KEY = 'test-secret'
    try:
        result = food_vision.analyze_image(b'image', 'image/png')
    finally:
        food_vision.requests.post = original
        settings.GEMINI_API_KEY = original_key
    assert result['portion_description'] == 'one bowl'
    assert result['estimated_carbohydrates_g'] == 48


def test_reported_canonical_nutrition_names_are_normalized():
    result = food_vision.normalize_analysis({
        'detected_food': 'Fresh Fruit Bowl',
        'serving_size': '1 large bowl',
        'calories': 420,
        'protein_g': 12,
        'carbohydrates_g': 65,
        'fat_g': 14,
        'fiber_g': 8,
        'ai_notes': 'Image-based estimate',
        'confidence': 0.8,
    })
    assert result['food_name'] == 'Fresh Fruit Bowl'
    assert result['portion_description'] == '1 large bowl'
    assert result['estimated_calories'] == 420
    assert result['estimated_protein_g'] == 12
    assert result['estimated_carbohydrates_g'] == 65
    assert result['estimated_fat_g'] == 14
    assert result['estimated_fiber_g'] == 8
    assert result['notes'] == 'Image-based estimate'
    assert result['confidence'] == 0.8


@pytest.mark.parametrize('status,expected', [
    (400, 'credentials or request configuration'),
    (401, 'credentials or request configuration'),
    (403, 'credentials or request configuration'),
    (404, 'model or API endpoint'),
    (429, 'rate limit or quota'),
    (500, 'temporarily unavailable'),
])
def test_http_errors_are_safe(monkeypatch, status, expected):
    monkeypatch.setattr(food_vision.requests, 'post', lambda *args, **kwargs: FakeResponse(status))
    monkeypatch.setattr(settings, 'GEMINI_API_KEY', 'secret-not-returned')

    with pytest.raises(food_vision.FoodVisionError) as error:
        food_vision.analyze_image(b'image', 'image/jpeg')
    assert expected in str(error.value)
    assert 'secret-not-returned' not in str(error.value)


def test_timeout_is_safe(monkeypatch):
    def timeout(*args, **kwargs):
        raise requests.Timeout('private timeout detail')

    monkeypatch.setattr(food_vision.requests, 'post', timeout)
    monkeypatch.setattr(settings, 'GEMINI_API_KEY', 'secret-not-returned')

    with pytest.raises(food_vision.FoodVisionError, match='timed out') as error:
        food_vision.analyze_image(b'image', 'image/jpeg')
    assert 'secret-not-returned' not in str(error.value)


def test_malformed_response_is_safe(monkeypatch):
    monkeypatch.setattr(food_vision.requests, 'post', lambda *args, **kwargs: valid_response('not-json'))
    monkeypatch.setattr(settings, 'GEMINI_API_KEY', 'secret-not-returned')

    with pytest.raises(food_vision.FoodVisionError, match='invalid or unavailable') as error:
        food_vision.analyze_image(b'image', 'image/jpeg')
    assert 'secret-not-returned' not in str(error.value)
