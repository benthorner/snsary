import json
import logging
import os
from pathlib import Path

import httpretty
import pytest

from snsary.contrib.google import BigQueryOutput


@pytest.fixture()
def credentials_path():
    return f"{Path(__file__).parent}/credentials.json"


@pytest.fixture
@httpretty.activate(allow_net_connect=False)
def big_query(mocker, credentials_path):
    mocker.patch.dict(os.environ, {
        'GOOGLE_APPLICATION_CREDENTIALS': credentials_path,
    })

    # body obtained by inspecting code and errors from returning an empty JSON response
    httpretty.register_uri(
        httpretty.POST,
        'https://oauth2.googleapis.com/token',
        body=json.dumps({"access_token": "1234", "expires_in": 33})
    )

    # body obtained by inspecting code and errors from returning an empty JSON response
    httpretty.register_uri(
        httpretty.GET,
        (
            'https://bigquery.googleapis.com/bigquery' +
            '/v2/projects/test-project/datasets/snsary/tables/readings?prettyPrint=false'
        ),
        body=json.dumps({
            "tableReference": {"tableId": "1234", "projectId": "1234", "datasetId": "1234"}
        })
    )

    return BigQueryOutput(retry_deadline=0)


@httpretty.activate(allow_net_connect=False)
def test_publish_batch(
    mocker,
    reading,
    big_query
):
    mocker.patch('platform.node', return_value='snsary')

    httpretty.register_uri(
        httpretty.POST,
        (
            'https://bigquery.googleapis.com/bigquery' +
            '/v2/projects/1234/datasets/1234/tables/1234/insertAll?prettyPrint=false'
        ),
    )

    big_query.publish_batch([reading])
    request = httpretty.last_request()

    assert b'"host": "snsary"' in request.body
    assert b'"metric": "myreading"' in request.body
    assert b'"sensor": "mysensor"' in request.body
    assert b'"timestamp": "2022-04-23T20:25:46+00:00"' in request.body
    assert b'"value": 123' in request.body


@httpretty.activate(allow_net_connect=False)
def test_publish_batch_error(big_query):
    httpretty.register_uri(
        httpretty.POST,
        (
            'https://bigquery.googleapis.com/bigquery' +
            '/v2/projects/1234/datasets/1234/tables/1234/insertAll?prettyPrint=false'
        ),
        status=500
    )

    with pytest.raises(Exception) as excinfo:
        big_query.publish_batch([])

    assert 'Deadline of 0.0s exceeded' in str(excinfo.value)


@httpretty.activate(allow_net_connect=False)
def test_publish_batch_invalid(caplog, big_query):
    caplog.set_level(logging.ERROR)

    httpretty.register_uri(
        httpretty.POST,
        (
            'https://bigquery.googleapis.com/bigquery' +
            '/v2/projects/1234/datasets/1234/tables/1234/insertAll?prettyPrint=false'
        ),
        body=json.dumps({
            'insertErrors': [{'index': 0, 'errors': [{'message': 'no such field: abc.'}]}]
        })
    )

    big_query.publish_batch([])
    assert 'Error inserting row' in caplog.text
    assert 'no such field' in caplog.text
