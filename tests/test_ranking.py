import os

# Use a test-local SQLite DB before app imports bind the engine.
os.environ["DATABASE_URL"] = "sqlite:///./test_offer_rank.db"

from fastapi.testclient import TestClient

from app.db import Base, engine, init_db
from app.main import app
from app.seed import seed_if_empty


def setup_module() -> None:
    Base.metadata.drop_all(bind=engine)
    init_db()
    seed_if_empty()


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_alex_prefers_grocery() -> None:
    response = client.get("/consumers/c_alex/recommendations?limit=3")
    assert response.status_code == 200
    body = response.json()
    assert body["consumer_id"] == "c_alex"
    assert len(body["ranked"]) >= 1
    top_categories = [row["offer"]["category"] for row in body["ranked"][:2]]
    assert "grocery" in top_categories


def test_unknown_consumer_404() -> None:
    response = client.get("/consumers/does_not_exist/recommendations")
    assert response.status_code == 404
