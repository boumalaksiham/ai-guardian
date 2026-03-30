from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_cost_computation():
    from app.services.cost_service import compute_cost
    cost = compute_cost("gpt-4o-mini", 100, 200)
    assert cost > 0

def test_evaluation_service():
    from app.services.evaluation_service import evaluate_output
    result = evaluate_output("What is AI?", "AI stands for Artificial Intelligence.")
    assert "quality_score" in result
    assert "hallucination_risk" in result
    assert "groundedness_score" in result