import pytest

from flaskapi.app import create_app
from flaskapi.models import _counter, _items


@pytest.fixture()
def app():
    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clear_store():
    _items.clear()
    _counter[0] = 0
    yield
    _items.clear()
    _counter[0] = 0


class TestListItems:
    def test_empty_returns_empty_list(self, client):
        resp = client.get("/items")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_returns_all_created_items(self, client):
        client.post("/items", json={"name": "A", "price": 1.0})
        client.post("/items", json={"name": "B", "price": 2.0})
        resp = client.get("/items")
        assert resp.status_code == 200
        assert len(resp.get_json()) == 2


class TestCreateItem:
    def test_success_returns_201(self, client):
        resp = client.post("/items", json={"name": "Widget", "price": 9.99})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Widget"
        assert data["price"] == 9.99
        assert "id" in data

    def test_missing_name_returns_400(self, client):
        resp = client.post("/items", json={"price": 9.99})
        assert resp.status_code == 400

    def test_invalid_price_returns_400(self, client):
        resp = client.post("/items", json={"name": "Widget", "price": -1})
        assert resp.status_code == 400

    def test_zero_price_returns_400(self, client):
        resp = client.post("/items", json={"name": "Widget", "price": 0})
        assert resp.status_code == 400


class TestGetItem:
    def test_found_returns_item(self, client):
        client.post("/items", json={"name": "Widget", "price": 9.99})
        resp = client.get("/items/1")
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Widget"

    def test_not_found_returns_404(self, client):
        resp = client.get("/items/999")
        assert resp.status_code == 404


class TestDeleteItem:
    def test_success_returns_204(self, client):
        client.post("/items", json={"name": "Widget", "price": 9.99})
        resp = client.delete("/items/1")
        assert resp.status_code == 204

    def test_deleted_item_no_longer_accessible(self, client):
        client.post("/items", json={"name": "Widget", "price": 9.99})
        client.delete("/items/1")
        assert client.get("/items/1").status_code == 404

    def test_not_found_returns_404(self, client):
        resp = client.delete("/items/999")
        assert resp.status_code == 404
