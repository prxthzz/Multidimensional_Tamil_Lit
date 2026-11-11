from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_health_endpoint():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "indexed_verses" in data

def test_api_concepts_endpoint():
    res = client.get("/api/v1/scientific/concepts")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] >= 50

def test_api_search_analyze_endpoint():
    payload = {
        "query": "How does rain support life?",
        "language": "english",
        "top_k": 3
    }
    res = client.post("/api/v1/search/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "relationship_type" in data
    assert "evidence_strength" in data
    assert "retrieval_relevance" in data
    assert "interpretation_confidence" in data
    assert len(data["tamil_evidence"]) > 0

def test_api_evaluation_latest_endpoint():
    res = client.get("/api/v1/evaluation/latest")
    assert res.status_code == 200
    data = res.json()
    assert "ablation_comparison" in data or "status" in data
