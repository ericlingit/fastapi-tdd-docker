from app.models.summary_payload import SummaryResponseSchema
import json
from typing import List

import pytest
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

    response = test_app.post("/summary", data=json.dumps({"url": "xxx://yyy"}))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"

    response = test_app.post("/summary", data=json.dumps({"url": "xxx"}))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "invalid or missing URL scheme"


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
    # Get non-existent record
    response = test_app_with_db.get("/summary/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    # Get id == 0
    response = test_app_with_db.get("/summary/0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


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

    response = test_app_with_db.delete("/summary/0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


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


@pytest.mark.parametrize("summary_id, payload, status_code, detail", [
    # Test non-existant id
    [
        999,
        {"url": "https://foo.bar", "summary": "updated!"},
        404, # Expected status_code
        "Summary not found"
    ],
    # Test id = 0
    [
        0,
        {"url": "https://foo.bar", "summary": "updated!"},
        422,
        [{
            "loc": ["path", "id"],
            "msg": "ensure this value is greater than 0",
            "type": "value_error.number.not_gt",
            "ctx": {"limit_value": 0}
        }]
    ],
    # Test json data: empty
    [
        1,
        {},
        422,
        [
            {"loc": ["body", "url"], "msg": "field required", "type": "value_error.missing"},
            {"loc": ["body", "summary"], "msg": "field required", "type": "value_error.missing"}
        ]
    ],
    # Test json data: missing 'summary' key
    [
        1,
        {"url": "https://foo.bar"},
        422,
        [{
            "loc": ["body", "summary"],
            "msg": "field required",
            "type": "value_error.missing"
        }]
    ],
    # Test json data: bad url
    [
        1,
        {"url": "xxx://yyy", "summary": "updated!"},
        422,
        [{
            "loc": ["body", "url"],
            "msg": "URL scheme not permitted",
            "type": "value_error.url.scheme",
            "ctx": {"allowed_schemes": ["http", "https"]}
        }]
    ]
])
def test_update_summary_bad_id_json(test_app_with_db: TestClient, summary_id, payload, status_code, detail):
    response = test_app_with_db.put(
        f"/summary/{summary_id}",
        data=json.dumps(payload)
    )
    assert response.status_code == status_code
    assert response.json()["detail"] == detail
