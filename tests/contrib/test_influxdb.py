import os

import httpretty
import pytest

from snsary.contrib.influxdb import InfluxDBOutput
from snsary.models import Reading
from snsary.sources import Sensor


@pytest.fixture()
def influxdb(mocker):
    mocker.patch('platform.node', return_value='snsary')

    return InfluxDBOutput(
        url='http://influxdb',
        token='token',
        org='org',
        bucket='bucket'
    )


@pytest.fixture()
def sensor():
    return Sensor(name='sensor')


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
    sensor
):
    httpretty.register_uri(
        httpretty.POST,
        'http://influxdb/api/v2/write?org=org&bucket=bucket&precision=s'
    )

    influxdb.publish_batch([
        Reading(
            sensor=sensor,
            name='metric',
            timestamp_seconds=1000,
            value=1
        )
    ])

    request = httpretty.last_request()
    assert request.headers['Authorization'] == 'Token token'
    assert b'metric,host=snsary,sensor=sensor value=1i 1000' in request.body
