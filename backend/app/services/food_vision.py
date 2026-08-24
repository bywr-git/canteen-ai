import base64
import json
import logging
from typing import Any

import requests

from ..config import settings

logger = logging.getLogger(__name__)


class FoodVisionError(Exception):
    """Raised when food image analysis cannot produce a safe result."""


ANALYSIS_PROMPT = """
Analyze only the food visibly present in this image and return JSON matching
this schema. Estimate portion size and nutrition; values are not medically
accurate. Do not invent hidden ingredients. Use null when a value cannot
reasonably be inferred. Communicate uncertainty in notes. If multiple foods
are clearly visible, include them in foods.
""".strip()

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
REQUEST_TIMEOUT_SECONDS = 30
RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "food_name": {"type": "STRING", "nullable": True},
        "serving_size": {"type": "STRING", "nullable": True},
        "calories": {"type": "NUMBER", "nullable": True},
        "protein_g": {"type": "NUMBER", "nullable": True},
        "carbohydrates_g": {"type": "NUMBER", "nullable": True},
        "fat_g": {"type": "NUMBER", "nullable": True},
        "fiber_g": {"type": "NUMBER", "nullable": True},
        "confidence": {"type": "NUMBER", "nullable": True},
        "notes": {"type": "STRING", "nullable": True},
        "foods": {"type": "ARRAY", "items": {"type": "OBJECT"}},
    },
}


def _number(value: Any):
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("boolean is not a nutrition number")
    return float(value)


def normalize_analysis(value: Any) -> dict:
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise ValueError("analysis must be an object")

    foods = value.get("foods")
    if foods is not None and not isinstance(foods, list):
        raise ValueError("foods must be a list")
    normalized_foods = []
    for food in foods or []:
        if not isinstance(food, dict):
            raise ValueError("each food must be an object")
        normalized_foods.append({
            "name": food.get("name"),
            "estimated_portion": food.get("estimated_portion"),
            "estimated_calories": _number(food.get("estimated_calories")),
            "protein_g": _number(food.get("protein_g", food.get("protein"))),
            "carbohydrates_g": _number(food.get("carbohydrates_g", food.get("carbohydrates"))),
            "fat_g": _number(food.get("fat_g", food.get("fat"))),
            "fiber_g": _number(food.get("fiber_g", food.get("fiber"))),
        })

    confidence = _number(value.get("confidence"))
    if confidence is not None and not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return {
        "food_name": value.get("detected_food", value.get("food_name")),
        "confidence": confidence,
        "portion_description": value.get("serving_size", value.get("portion_description")),
        "estimated_calories": _number(value.get("calories", value.get("estimated_calories"))),
        "estimated_protein_g": _number(value.get("protein_g", value.get("estimated_protein"))),
        "estimated_carbohydrates_g": _number(value.get("carbohydrates_g", value.get("estimated_carbohydrates"))),
        "estimated_fat_g": _number(value.get("fat_g", value.get("estimated_fat"))),
        "estimated_fiber_g": _number(value.get("fiber_g", value.get("estimated_fiber"))),
        "notes": value.get("ai_notes", value.get("notes")),
        "foods": normalized_foods,
    }


def _raise_for_status(response):
    if response.status_code in (400, 401, 403):
        raise FoodVisionError("Gemini API credentials or request configuration are invalid")
    if response.status_code == 404:
        raise FoodVisionError("Configured Gemini model or API endpoint was not found")
    if response.status_code == 429:
        raise FoodVisionError("Gemini API rate limit or quota exceeded")
    if response.status_code >= 500:
        raise FoodVisionError("Gemini service is temporarily unavailable")
    response.raise_for_status()


def _sanitize_diagnostic_message(message: Any) -> str:
    sanitized = str(message or "").replace(settings.GEMINI_API_KEY, "[redacted]")
    return " ".join(sanitized.split())[:300]


def _log_response_diagnostics(url: str, response):
    content_type = response.headers.get("Content-Type", "") if getattr(response, "headers", None) else ""
    logger.info("GEMINI_REQUEST_URL=%s", url)
    logger.info("GEMINI_HTTP_STATUS=%s", response.status_code)
    logger.info("GEMINI_CONTENT_TYPE=%s", _sanitize_diagnostic_message(content_type))
    if response.status_code >= 400:
        error_type = "HTTPError"
        error_message = "HTTP %s" % response.status_code
        try:
            error_payload = response.json().get("error", {})
            if isinstance(error_payload, dict):
                error_type = error_payload.get("status") or error_payload.get("reason") or error_type
                error_message = error_payload.get("message") or error_message
        except (ValueError, TypeError, AttributeError):
            pass
        logger.warning("GEMINI_ERROR_TYPE=%s", _sanitize_diagnostic_message(error_type))
        logger.warning("GEMINI_ERROR_MESSAGE=%s", _sanitize_diagnostic_message(error_message))


def _configured_model_name() -> str:
    model = settings.GEMINI_MODEL.strip()
    if not model or model.startswith("models/") or "/v1beta/" in model or ":generateContent" in model or "/" in model:
        raise FoodVisionError("Gemini model configuration is invalid")
    return model


def analyze_image(image_bytes: bytes, mime_type: str) -> dict:
    if not settings.GEMINI_API_KEY:
        raise FoodVisionError("Food scanner is not configured")

    payload = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode("ascii")}},
                {"text": ANALYSIS_PROMPT},
            ],
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
        },
    }
    url = GEMINI_ENDPOINT.format(model=_configured_model_name())
    try:
        response = requests.post(
            url,
            params={"key": settings.GEMINI_API_KEY},
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        _log_response_diagnostics(url, response)
        _raise_for_status(response)
        response_data = response.json()
        text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        return normalize_analysis(text)
    except FoodVisionError:
        raise
    except requests.Timeout as exc:
        logger.warning("GEMINI_REQUEST_URL=%s", url)
        logger.warning("GEMINI_ERROR_TYPE=Timeout")
        logger.warning("GEMINI_ERROR_MESSAGE=Gemini request timed out")
        raise FoodVisionError("Gemini analysis timed out; please try again") from exc
    except requests.RequestException as exc:
        logger.warning("GEMINI_REQUEST_URL=%s", url)
        logger.warning("GEMINI_ERROR_TYPE=%s", _sanitize_diagnostic_message(type(exc).__name__))
        logger.warning("GEMINI_ERROR_MESSAGE=%s", _sanitize_diagnostic_message(str(exc)))
        raise FoodVisionError("Gemini returned an invalid or unavailable analysis") from exc
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        logger.warning("GEMINI_REQUEST_URL=%s", url)
        logger.warning("GEMINI_ERROR_TYPE=%s", _sanitize_diagnostic_message(type(exc).__name__))
        logger.warning("GEMINI_ERROR_MESSAGE=%s", _sanitize_diagnostic_message(str(exc)))
        raise FoodVisionError("Gemini returned an invalid or unavailable analysis") from exc
