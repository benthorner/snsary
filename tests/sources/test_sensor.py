from snsary.sources import Sensor


def test_subscribe(mocker):
    sensor = Sensor(name='foo')
    mock_stream = mocker.patch.object(sensor.stream, 'subscribe')
    sensor.subscribe('output')
    mock_stream.assert_called_with('output')
