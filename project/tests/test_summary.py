import json
from typing import List

from starlette.testclient import TestClient


def test_create_summary(test_app_with_db: TestClient):
    """Fixture for this test is located at conftest.test_app_with_db()."""
    response = test_app_with_db.post("/summary", data=json.dumps({"url": "https://foo.bar"}))

    assert response.status_code == 201
    assert response.json().get("url", "") == "https://foo.bar"


def test_create_summary_bad_json(test_app: TestClient):
    response = test_app.post("/summary", data=json.dumps({}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["body", "url"], "msg": "field required", "type": "value_error.missing"}]
    }


def test_read_summary(test_app_with_db: TestClient):
    response = test_app_with_db.post("/summary", data=json.dumps({"url": "https://foo.bar"}))
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summary/{summary_id}")
    assert response.status_code == 200

    rj = response.json()
    assert rj["id"] == summary_id
    assert rj["url"] == "https://foo.bar"
    assert rj["summary"]
    assert rj["created_at"]


def test_read_summary_bad_id(test_app_with_db: TestClient):
    response = test_app_with_db.get("/summary/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app_with_db: TestClient):
    response = test_app_with_db.post("/summary", data=json.dumps({"url": "https://foo.bar"}))
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summary")
    assert response.status_code == 200

    rj: List[dict] = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, rj))) == 1


def test_remove_summary(test_app_with_db: TestClient):
    response = test_app_with_db.post(
        '/summary',
        data=json.dumps({'url': 'https://foo.bar'})
    )
    summary_id = response.json()['id']

    response = test_app_with_db.delete(f'/summary/{summary_id}')
    assert response.status_code == 200
    assert response.json() == {'id': summary_id, 'url': 'https://foo.bar'}


def test_remove_summary_bad_id(test_app_with_db: TestClient):
    response = test_app_with_db.delete('/summary/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Summary not found'


def test_update_summary(test_app_with_db: TestClient):
    response = test_app_with_db.post(
        "/summary",
        data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()['id']

    response = test_app_with_db.put(
        f"/summary/{summary_id}",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"})
    )
    assert response.status_code == 200

    rj = response.json()
    assert rj["id"] == summary_id
    assert rj["url"] == "https://foo.bar"
    assert rj["summary"] == "updated!"
    assert rj["created_at"]


def test_update_summary_bad_id(test_app_with_db: TestClient):
    response = test_app_with_db.put(
        "/summary/999",
        data=json.dumps({"url": "https://foo.bar", "summary": "updated!"})
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary_bad_json(test_app_with_db: TestClient):
    response = test_app_with_db.post(
        "/summary",
        data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summary/{summary_id}",
        data=json.dumps({})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_update_summary_bad_json_keys(test_app_with_db: TestClient):
    response = test_app_with_db.post(
        "/summary",
        data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summary/{summary_id}",
        data=json.dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "summary"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
