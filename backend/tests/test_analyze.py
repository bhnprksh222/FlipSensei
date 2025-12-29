from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_analyze_good_flip():
    payload = {
        "title": "Dell 27-inch Monitor",
        "price": 120,
        "location": "Austin, TX",
        "url": "https://www.facebook.com/marketplace/item/123456789",
    }
    response = client.post("/analyze", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["estimated_resale_price"] > payload["price"]
    assert data["estimated_profit"] > 0
    assert data["roi_percent"] > 0
    assert data["recommendation"] in ["GOOD_FLIP", "MAYBE", "PASS"]
    assert "notes" in data


def test_analyze_invalid_url():
    payload = {
        "title": "Monitor",
        "price": 100,
        "location": "NY",
        "url": "https://google.com/item/123",
    }

    response = client.post("/analyze", json=payload)

    assert response.status_code == 422


def test_analyze_invalid_price():
    payload = {
        "title": "Monitor",
        "price": 0,
        "location": "NY",
        "url": "https://www.facebook.com/marketplace/item/123",
    }

    response = client.post("/analyze", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert body["detail"][0]["loc"] == ["body", "price"]


def test_request_id_header_present():
    payload = {
        "title": "Monitor",
        "price": 100,
        "location": "NY",
        "url": "https://www.facebook.com/marketplace/item/123",
    }

    response = client.post("/analyze", json=payload)

    assert "X-Request-ID" in response.headers
