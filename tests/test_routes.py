import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_create_and_get_task(client):
    res = client.post("/tasks", json={"title": "Tugas 1"})
    assert res.status_code == 201
    assert client.get("/tasks/1").get_json()["title"] == "Tugas 1"


def test_create_invalid_title(client):
    res = client.post("/tasks", json={"title": ""})
    assert res.status_code == 400


def test_update_done(client):
    client.post("/tasks", json={"title": "Tugas"})
    res = client.put("/tasks/1", json={"done": True})
    assert res.get_json()["done"] is True
    assert len(client.get("/tasks?done=true").get_json()) == 1


def test_delete_and_404(client):
    client.post("/tasks", json={"title": "Tugas"})
    assert client.delete("/tasks/1").status_code == 204
    assert client.get("/tasks/1").status_code == 404


def test_index_page_served(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Task Manager" in res.data


def test_static_assets_served(client):
    assert client.get("/static/style.css").status_code == 200
    assert client.get("/static/app.js").status_code == 200
