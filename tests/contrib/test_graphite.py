import json

import httpretty
import pytest

from snsary.contrib.graphite import GraphiteOutput
from snsary.models import Reading
from snsary.sensors import Sensor


@pytest.fixture()
def graphite(mocker):
    mocker.patch('platform.node', return_value='snsary')
    return GraphiteOutput(url='http://graphite')


@pytest.fixture()
def sensor():
    return Sensor(name='sensor')


@httpretty.activate(allow_net_connect=False)
def test_send_batch(
    graphite,
    sensor
):
    httpretty.register_uri(
        httpretty.POST,
        'http://graphite/'
    )

    graphite.send_batch([
        Reading(
            sensor=sensor,
            name='metric',
            timestamp_seconds=1000,
            value=1
        )
    ])

    request = httpretty.last_request()

    assert json.loads(request.body) == [{
        'interval': 1,
        'name': 'snsary.sensor.metric',
        'time': 1000,
        'value': 1
    }]


@httpretty.activate(allow_net_connect=False)
def test_send_batch_error(
    graphite,
    sensor
):
    httpretty.register_uri(
        httpretty.POST,
        'http://graphite/',
        status=500
    )

    with pytest.raises(Exception) as excinfo:
        graphite.send_batch([])

    assert '500 Server Error' in str(excinfo.value)
