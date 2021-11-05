import base64
import json
import re
from datetime import datetime

import httpretty
import pytest
from freezegun import freeze_time

from snsary.contrib.octopus import OctopusSensor


@pytest.fixture
def sensor():
    return OctopusSensor(
        mpan='mpan',
        serial_number='serial_number',
        token='token-123'
    )


@freeze_time("2021-11-05 15:32:23.1234")
@httpretty.activate(allow_net_connect=False)
def test_sample(
    sensor
):
    url = OctopusSensor.CONSUMPTION_URL.format(**{
        'mpan': 'mpan',
        'serial_number': 'serial_number',
        'period_from': '2021-11-04T00:00:00'
    })

    httpretty.register_uri(
        httpretty.GET,
        url,
        match_querystring=True,
        body=json.dumps({
            'results': [{
                "consumption": 0.076,
                "interval_start": "2021-11-04T23:00:00Z",
                "interval_end": "2021-11-04T23:30:00Z"
            }]
        })
    )

    readings = sensor.sample(now=datetime.utcnow())
    assert len(readings) == 1

    assert readings[0].value == 0.076
    assert readings[0].sensor == sensor
    assert readings[0].name == 'consumption'
    assert datetime.fromtimestamp(readings[0].timestamp).minute == 30

    request = httpretty.last_request()
    auth = base64.b64encode(b'token-123:').decode('utf-8')
    assert request.headers['Authorization'] == f'Basic {auth}'


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
