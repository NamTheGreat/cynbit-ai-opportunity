import pytest
from fastapi.testclient import TestClient
from aria_evaluator.api import app

client = TestClient(app)


def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_api_rubrics():
    res = client.get("/api/v1/rubrics")
    assert res.status_code == 200
    assert "weights" in res.json()
    assert "thresholds" in res.json()


def test_api_evaluate_code():
    payload = {
        "target_name": "API Test Submission",
        "role_target": "Backend Developer",
        "files": {
            "main.py": "def add(a, b): return a + b"
        }
    }
    res = client.post("/api/v1/evaluate/code", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "overall_score" in data
    assert "recommendation" in data
    assert "dimension_scores" in data
