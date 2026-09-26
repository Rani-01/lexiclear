from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from core.config import DISCLAIMER_TEXT

client = TestClient(app)

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert "disclaimer" in body

def test_security_headers_present():
    res = client.get("/api/health")
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    assert res.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in res.headers

def test_analyze_validation_empty_and_short():
    # Fails min_length
    res = client.post("/api/analyze", json={"document_text": "too short"})
    assert res.status_code == 422

def test_analyze_validation_oversized():
    # Fails max_length bounds
    oversized = "a" * 50001
    res = client.post("/api/analyze", json={"document_text": oversized})
    assert res.status_code == 422

@patch("main.analyze_document")
def test_analyze_success_and_caching(mock_analyze):
    mock_analyze.return_value = {
        "summary": "Tenant pays rent on 1st.",
        "reading_level": "Plain English",
        "key_obligations": ["Pay rent"],
        "risks_and_flags": [],
        "action_checklist": [],
        "questions_for_lawyer": []
    }
    payload = {"document_text": "This agreement requires tenant to pay rent on the 1st of every month without fail."}
    
    # First call: fresh compute
    res1 = client.post("/api/analyze", json=payload)
    assert res1.status_code == 200
    assert res1.json()["cached"] is False
    assert mock_analyze.call_count == 1

    # Second call with identical payload: should hit cache
    res2 = client.post("/api/analyze", json=payload)
    assert res2.status_code == 200
    assert res2.json()["cached"] is True
    assert mock_analyze.call_count == 1  # No extra LLM call

@patch("main.compare_documents")
def test_compare_success(mock_compare):
    mock_compare.return_value = {
        "key_differences": [{"aspect": "Notice", "doc_a_position": "30 days", "doc_b_position": "60 days", "impact": "Doc B gives more notice"}],
        "favorable_to": "Document B",
        "negotiation_recommendations": ["Align on 45 days"]
    }
    res = client.post("/api/compare", json={"doc_a": "Notice period shall be 30 days.", "doc_b": "Notice period shall be 60 days."})
    assert res.status_code == 200
    assert res.json()["data"]["favorable_to"] == "Document B"

@patch("main.ask_question")
def test_ask_success(mock_ask):
    mock_ask.return_value = "Yes, early termination incurs a one month penalty fee."
    res = client.post("/api/ask", json={
        "document_text": "Early termination fee is one month rent.",
        "question": "Is there a fee for breaking lease?"
    })
    assert res.status_code == 200
    assert "one month penalty" in res.json()["answer"]