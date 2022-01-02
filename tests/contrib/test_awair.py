import json
import os
import re
from datetime import datetime

import httpretty
import pytest
from freezegun import freeze_time

from snsary.contrib.awair import AwairSensor


@pytest.fixture
def sensor():
    return AwairSensor(
        device_type='awair-r2',
        device_id='1234',
        token='token-123'
    )


def test_discover_from_env(mocker):
    mocker.patch.dict(os.environ, {
        'AWAIR_TOKEN': 'token'
    })

    mock_discover = mocker.patch.object(
        AwairSensor, 'discover', return_value='instances'
    )

    assert AwairSensor.discover_from_env() == 'instances'
    mock_discover.assert_called_with(token='token')


@httpretty.activate(allow_net_connect=False)
def test_discover():
    httpretty.register_uri(
        httpretty.GET,
        AwairSensor.DEVICES_URL,
        body=json.dumps({
            'devices': [{
                'deviceType': 'awair-r2',
                'deviceId': '1234'
            }]
        })
    )

    sensors = AwairSensor.discover(token='token-123')
    assert len(sensors) == 1
    assert(sensors[0].name) == 'awair-r2-1234'

    request = httpretty.last_request()
    assert request.headers['Authorization'] == 'Bearer token-123'


@httpretty.activate(allow_net_connect=False)
def test_discover_error():
    httpretty.register_uri(
        httpretty.GET,
        AwairSensor.DEVICES_URL,
        status=500,
    )

    with pytest.raises(Exception) as excinfo:
        AwairSensor.discover(token='token-123')

    assert '500 Server Error' in str(excinfo.value)


@freeze_time("2021-11-05 12:00:00")
@httpretty.activate(allow_net_connect=False)
def test_sample(
    sensor
):
    url = AwairSensor.DATA_URL.format(**{
        'deviceType': 'awair-r2',
        'deviceId': '1234',
        'from': '2021-11-05T11:50:00'
    })

    httpretty.register_uri(
        httpretty.GET,
        url,
        match_querystring=True,
        body=json.dumps({
            'data': [{
                'timestamp': '2021-11-05T11:55:00.000Z',
                'sensors': [{'comp': 'temp', 'value': 123}]
            }]
        })
    )

    readings = sensor.sample(now=datetime.utcnow())
    assert len(readings) == 1

    assert readings[0].value == 123
    assert readings[0].sensor == sensor
    assert readings[0].name == 'temp'
    assert datetime.fromtimestamp(readings[0].timestamp).minute == 55

    request = httpretty.last_request()
    assert request.headers['Authorization'] == 'Bearer token-123'


@freeze_time("2021-11-05 12:00:00")
@httpretty.activate(allow_net_connect=False)
def test_sample_error(
    sensor
):
    httpretty.register_uri(
        httpretty.GET,
        re.compile(".*"),
        status=500,
    )

    with pytest.raises(Exception) as excinfo:
        sensor.sample(now=datetime.utcnow())

    assert '500 Server Error' in str(excinfo.value)