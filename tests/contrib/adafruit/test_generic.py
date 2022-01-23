import pytest

from snsary.contrib.adafruit import GenericSensor


@pytest.fixture
def mock_device():
    class MockDevice:
        @property
        def data(self):
            return 1.23

    return MockDevice()


@pytest.fixture
def sensor(mock_device):
    return GenericSensor(mock_device)


def test_name(sensor):
    assert sensor.name == 'MockDevice'


def test_sample(sensor, mock_device):
    readings = list(sensor.sample(
        timestamp_seconds='now'
    ))

    assert len(readings) == 1
    assert readings[0].name == 'data'
    assert readings[0].value == 1.23
    assert readings[0].sensor == sensor
    assert readings[0].timestamp == 'now'


def test_sample_not_ready(sensor):
    sensor.ready = lambda kwarg: False
    assert not sensor.sample(kwarg=1)
