import json
import os

import httpretty
import pytest

from snsary.contrib.grafana import GraphiteOutput


@pytest.fixture()
def graphite():
    return GraphiteOutput(
        url='http://graphite', prefix='snsary'
    )


def test_from_env(mocker):
    mocker.patch.dict(os.environ, {'GRAPHITE_URL': 'url'})
    mocker.patch('platform.node', return_value='snsary')

    mock_init = mocker.patch.object(
        GraphiteOutput, '__init__',
        return_value=None  # required to mock __init__
    )

    assert isinstance(GraphiteOutput.from_env(), GraphiteOutput)
    mock_init.assert_called_with(url='url', prefix='snsary')


@httpretty.activate(allow_net_connect=False)
def test_publish_batch(
    graphite,
    sensor,
    reading
):
    httpretty.register_uri(
        httpretty.POST,
        'http://graphite/'
    )

    graphite.publish_batch([reading])
    request = httpretty.last_request()

    assert json.loads(request.body) == [{
        'interval': 1,
        'name': 'snsary.mysensor.myreading',
        'time': 123,
        'value': 123
    }]


@httpretty.activate(allow_net_connect=False)
def test_publish_batch_error(
    graphite,
    sensor,
    reading
):
    httpretty.register_uri(
        httpretty.POST,
        'http://graphite/',
        status=500
    )

    with pytest.raises(Exception) as excinfo:
        graphite.publish_batch([reading])

    assert '500 Server Error' in str(excinfo.value)
