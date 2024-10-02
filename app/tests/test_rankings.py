from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app
from app.db.session import SessionLocal
from app.models.models import Metric, LLM, SimulationResult, Ranking

client = TestClient(app)

def test_get_rankings_success():
    # Setup test data
    db = SessionLocal()
    metric = Metric(name="TTFT")
    llm = LLM(name="Test LLM")
    db.add(metric)
    db.add(llm)
    db.commit()
    db.refresh(metric)
    db.refresh(llm)
    simulation = SimulationResult(
        llm_id=llm.id,
        metric_id=metric.id,
        value=0.5,
        timestamp=datetime.utcnow()
    )
    db.add(simulation)
    db.commit()
    db.close()

    response = client.get("/api/v1/rankings/TPS/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["llm"] == "Test LLM"
    assert response.json()[0]["mean_value"] == 0.5
    assert response.json()[0]["rank"] == 1

def test_get_rankings_metric_not_found():
    response = client.get("/api/v1/rankings/NonExistentMetric/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Metric not found or no rankings available."
