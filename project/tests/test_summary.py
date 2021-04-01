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
