import json

import pytest


def test_create_summary(test_app_with_db):
    '''Fixture for this test is located at conftest.test_app_with_db().'''
    response = test_app_with_db.post(
        '/summary',
        data=json.dumps({'url': 'https://foo.bar'})
    )

    assert response.status_code == 201
    assert response.json().get('url', '') == 'https://foo.bar'


def test_create_summary_bad_json(test_app):
    response = test_app.post(
        '/summary',
        data=json.dumps({})
    )

    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'url'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }


def test_read_summary(test_app_with_db):
    response = test_app_with_db.post(
        '/summary',
        data=json.dumps({'url': 'https://foo.bar'})
    )
    summary_id = response.json()['id']

    response = test_app_with_db.get(
        f'/summary/{summary_id}'
    )
    assert response.status_code == 200

    rj = response.json()
    assert rj['id'] == summary_id
    assert rj['url'] == 'https://foo.bar'
    assert rj['summary']
    assert rj['created_at']