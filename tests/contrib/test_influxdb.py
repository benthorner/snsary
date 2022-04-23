import os

import httpretty
import pytest

from snsary.contrib.influxdb import InfluxDBOutput


@pytest.fixture()
def influxdb(mocker):
    mocker.patch('platform.node', return_value='snsary')

    return InfluxDBOutput(
        url='http://influxdb',
        token='token',
        org='org',
        bucket='bucket'
    )


def test_from_env(mocker):
    mocker.patch.dict(os.environ, {
        'INFLUXDB_URL': 'url',
        'INFLUXDB_TOKEN': 'token',
        'INFLUXDB_ORG': 'org',
        'INFLUXDB_BUCKET': 'bucket'
    })

    mock_init = mocker.patch.object(
        InfluxDBOutput, '__init__',
        return_value=None  # required to mock __init__
    )

    assert isinstance(
        InfluxDBOutput.from_env(), InfluxDBOutput
    )

    mock_init.assert_called_with(
        url='url',
        token='token',
        org='org',
        bucket='bucket'
    )


@httpretty.activate(allow_net_connect=False)
def test_publish_batch(
    influxdb,
    sensor,
    reading
):
    httpretty.register_uri(
        httpretty.POST,
        'http://influxdb/api/v2/write?org=org&bucket=bucket&precision=s'
    )

    influxdb.publish_batch([reading])
    request = httpretty.last_request()

    assert request.headers['Authorization'] == 'Token token'
    assert b'myreading,host=snsary,sensor=mysensor value=123i 1650745546' in request.body


@httpretty.activate(allow_net_connect=False)
def test_publish_batch_error(
    influxdb,
    sensor,
    reading
):
    httpretty.register_uri(
        httpretty.POST,
        'http://influxdb/api/v2/write?org=org&bucket=bucket&precision=s',
        status=500
    )

    with pytest.raises(Exception) as excinfo:
        influxdb.publish_batch([reading])

    assert 'Internal Server Error' in str(excinfo.value)
