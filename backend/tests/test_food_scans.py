import os
from uuid import uuid4

os.environ["TESTING"] = "true"

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app import models
from app.security import hash_password
from app.services import food_vision

client = TestClient(app)
JPEG = b"\xff\xd8\xff" + b"food-image"


def student(label):
    email = f"{label}-{uuid4().hex[:8]}@example.com"
    registered = client.post("/auth/register", json={
        "name": label, "email": email, "password": "Password123!",
        "department": "CS", "year": 2,
    })
    assert registered.status_code == 201
    user = registered.json()["user"]
    logged_in = client.post("/auth/login", json={
        "email": email, "password": "Password123!",
    })
    return user, {"Authorization": f"Bearer {logged_in.json()['access_token']}"}


def catalog_item():
    db = SessionLocal()
    item = models.FoodItem(
        name="Scan Catalogue Item", category="Meal", price=50,
        calories=100, protein=5, carbs=10, fat=2, fiber=1, sugar=1,
        is_available=True,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    item_id = item.item_id
    db.close()
    return item_id


def test_scanner_requires_auth_and_validates_upload(monkeypatch):
    assert client.post("/food-scans/analyze", files={"image": ("food.jpg", JPEG, "image/jpeg")}).status_code == 401
    assert client.post("/food-scans/analyze", files={"image": ("food.txt", b"text", "text/plain")}).status_code == 401
    _, headers = student("validation")
    assert client.post("/food-scans/analyze", headers=headers, files={"image": ("food.txt", b"text", "text/plain")}).status_code == 400
    oversized = b"\xff\xd8\xff" + b"x" * (5 * 1024 * 1024)
    assert client.post("/food-scans/analyze", headers=headers, files={"image": ("large.jpg", oversized, "image/jpeg")}).status_code == 413


def test_valid_scan_is_mocked_saved_and_not_purchased(monkeypatch):
    _, headers = student("scan")
    calls = []
    def mocked_analysis(data, mime_type):
        calls.append((data, mime_type))
        return {
            "food_name": "Masala Dosa", "confidence": 0.82,
            "portion_description": "1 serving", "estimated_calories": 400,
            "estimated_protein_g": 10, "estimated_carbohydrates_g": 55,
            "estimated_fat_g": 14, "estimated_fiber_g": 4,
            "notes": "Image-based estimate; not medically accurate.", "foods": [],
        }
    monkeypatch.setattr(food_vision, "analyze_image", mocked_analysis)
    response = client.post("/food-scans/analyze", headers=headers, files={"image": ("food.jpg", JPEG, "image/jpeg")})
    assert response.status_code == 201
    scan = response.json()
    assert calls == [(JPEG, "image/jpeg")]
    assert scan["detected_food_name"] == "Masala Dosa"
    assert scan["status"] == "pending_review"

    history = client.get("/food-scans", headers=headers)
    assert history.status_code == 200
    assert history.json()[0]["scan_id"] == scan["scan_id"]

    # Analysis alone does not create a purchase.
    assert client.get("/purchases", headers=headers).json() == []


def test_analyze_endpoint_returns_all_normalized_nutrition_values(monkeypatch):
    _, headers = student("nutrition-fields")
    monkeypatch.setattr(food_vision, "analyze_image", lambda *_: {
        "food_name": "Fresh Fruit Bowl",
        "confidence": 0.8,
        "portion_description": "1 large bowl",
        "estimated_calories": 420,
        "estimated_protein_g": 12,
        "estimated_carbohydrates_g": 65,
        "estimated_fat_g": 14,
        "estimated_fiber_g": 8,
        "notes": "Image-based estimate",
        "foods": [],
    })

    response = client.post(
        "/food-scans/analyze",
        headers=headers,
        files={"image": ("fruit.jpg", JPEG, "image/jpeg")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["detected_food_name"] == "Fresh Fruit Bowl"
    assert body["portion_description"] == "1 large bowl"
    assert body["estimated_calories"] == 420
    assert body["estimated_protein"] == 12
    assert body["estimated_carbohydrates"] == 65
    assert body["estimated_fat"] == 14
    assert body["estimated_fiber"] == 8
    assert body["analysis_notes"] == "Image-based estimate"
    assert body["confidence"] == 0.8
def test_malformed_and_provider_failures_are_safe(monkeypatch):
    _, headers = student("failure")
    monkeypatch.setattr(food_vision, "analyze_image", lambda *_: (_ for _ in ()).throw(food_vision.FoodVisionError("provider unavailable")))
    response = client.post("/food-scans/analyze", headers=headers, files={"image": ("food.jpg", JPEG, "image/jpeg")})
    assert response.status_code == 503
    assert "provider unavailable" in response.json()["detail"]

    monkeypatch.setattr(food_vision, "analyze_image", lambda *_: (_ for _ in ()).throw(ValueError("malformed")))
    response = client.post("/food-scans/analyze", headers=headers, files={"image": ("food.jpg", JPEG, "image/jpeg")})
    assert response.status_code == 502
def test_scan_ownership_confirmation_and_optional_purchase(monkeypatch):
    user_a, headers_a = student("owner-a")
    _, headers_b = student("owner-b")
    item_id = catalog_item()
    monkeypatch.setattr(food_vision, "analyze_image", lambda *_: {
        "food_name": "Scan Catalogue Item", "confidence": 0.7,
        "portion_description": "one serving", "estimated_calories": 100,
        "estimated_protein_g": 5, "estimated_carbohydrates_g": 10,
        "estimated_fat_g": 2, "estimated_fiber_g": 1,
        "notes": "Estimate only", "foods": [],
    })
    scan = client.post("/food-scans/analyze", headers=headers_a, files={"image": ("food.jpg", JPEG, "image/jpeg")}).json()
    scan_id = scan["scan_id"]

    assert client.get(f"/food-scans/{scan_id}", headers=headers_b).status_code == 404
    assert client.post(f"/food-scans/{scan_id}/confirm", headers=headers_b, json={}).status_code == 404

    confirmed = client.post(f"/food-scans/{scan_id}/confirm", headers=headers_a, json={
        "detected_food_name": "Edited Food", "add_to_purchases": True,
        "food_item_id": item_id, "quantity": 2,
    })
    assert confirmed.status_code == 200
    assert confirmed.json()["scan"]["status"] == "confirmed"
    assert confirmed.json()["purchase_id"]
    purchases = client.get("/purchases", headers=headers_a).json()
    assert len(purchases) == 1
    assert purchases[0]["user_id"] == user_a["user_id"]
    assert purchases[0]["total_price"] == 100


def test_failed_scan_does_not_invalidate_authentication(monkeypatch):
    user, headers = student("regression")
    monkeypatch.setattr(food_vision, "analyze_image", lambda *_: (_ for _ in ()).throw(
        food_vision.FoodVisionError("Configured Gemini model or API endpoint was not found")
    ))

    failed = client.post(
        "/food-scans/analyze",
        headers=headers,
        files={"image": ("food.jpg", JPEG, "image/jpeg")},
    )
    assert failed.status_code == 503
    assert failed.json()["detail"] == "Configured Gemini model or API endpoint was not found"

    me = client.get("/users/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["user_id"] == user["user_id"]
    assert client.get("/dashboard", headers=headers).status_code == 200

    relogin = client.post("/auth/login", json={
        "email": user["email"], "password": "Password123!"
    })
    assert relogin.status_code == 200

    second = client.post(
        "/food-scans/analyze",
        headers=headers,
        files={"image": ("food.jpg", JPEG, "image/jpeg")},
    )
    assert second.status_code == 503
