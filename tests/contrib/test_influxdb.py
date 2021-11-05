import httpretty
import pytest

from snsary.contrib.influxdb import InfluxDBOutput
from snsary.models import Reading
from snsary.sensors import Sensor


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


@httpretty.activate(allow_net_connect=False)
def test_send_batch(
    influxdb,
    sensor
):
    httpretty.register_uri(
        httpretty.POST,
        'http://influxdb/api/v2/write?org=org&bucket=bucket&precision=s'
    )

    influxdb.send_batch([
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
