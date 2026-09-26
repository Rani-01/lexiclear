from fastapi.testclient import TestClient
from main import app
from core.config import DISCLAIMER_TEXT

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert "disclaimer" in res.json()

def test_analyze_validation():
    # Tests that short text fails validation
    res = client.post("/api/analyze", json={"document_text": "short"})
    assert res.status_code == 422

def test_disclaimer_presence():
    assert "does not constitute formal legal advice" in DISCLAIMER_TEXT