import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_get():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs_url" in data
    assert "health_check" in data


def test_root_head():
    response = client.head("/")
    assert response.status_code == 200
    assert response.text == ""


def test_health_get_and_head():
    get_res = client.get("/api/v1/health")
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "healthy"

    head_res = client.head("/api/v1/health")
    assert head_res.status_code == 200
    assert head_res.text == ""
