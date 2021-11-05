import pytest

from snsary.contrib.adafruit import AdafruitSensor


@pytest.fixture
def mock_device(mocker):
    class MockDevice:
        @property
        def data(self):
            return 1.23

    return MockDevice()


@pytest.fixture
def sensor(mock_device):
    return AdafruitSensor(
        mock_device,
        ready_fn=lambda device: device.data_available,
    )


def test_sample_no_data(sensor, mock_device):
    mock_device.data_available = False

    with pytest.raises(RuntimeError) as excinfo:
        list(sensor.sample('now'))

    assert str(excinfo.value) == 'Device has no data to read.'


def test_init(sensor):
    assert sensor.name == 'MockDevice'


def test_sample(sensor, mock_device):
    mock_device.data_available = True
    readings = list(sensor.sample('now'))
    assert len(readings) == 1

    assert readings[0].name == 'data'
    assert readings[0].value == 1.23
    assert readings[0].sensor == sensor
    assert readings[0].timestamp == 'now'
