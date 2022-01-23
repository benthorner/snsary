import pytest

from snsary.contrib.adafruit.sgp30 import SGP30Sensor
from tests.conftest import create_reading


@pytest.fixture
def mock_sgp30(mocker):
    mock_class = mocker.patch(
        'adafruit_sgp30.Adafruit_SGP30', autospec=True
    )

    return mock_class('i2c')


@pytest.fixture
def sensor(mock_sgp30):
    return SGP30Sensor(mock_sgp30)


def test_ready(sensor):
    assert not sensor.ready(elapsed_seconds=15)
    assert sensor.ready(elapsed_seconds=16)


def test_publish_batch(sensor, mock_sgp30):
    sensor.publish_batch([
        create_reading(name='temperature'),
        create_reading(name='relative_humidity')
    ])

    mock_sgp30.set_iaq_humidity.assert_called_with(
        pytest.approx(1530.766)
    )


@pytest.mark.parametrize('readings', [
    [create_reading(name='temperature')],
    [create_reading(name='relative_humidity')],
    []
])
def test_publish_batch_incomplete(sensor, mock_sgp30, readings):
    sensor.publish_batch(readings)
    mock_sgp30.set_iaq_humidity.assert_not_called()
