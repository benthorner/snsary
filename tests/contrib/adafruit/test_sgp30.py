import pytest

from snsary.contrib.adafruit.sgp30 import SGP30Sensor
from snsary.utils.tracker import MaxTracker, NullTracker
from tests.conftest import create_reading


@pytest.fixture
def mock_sgp30(mocker):
    mock_class = mocker.patch(
        'adafruit_sgp30.Adafruit_SGP30', autospec=True
    )

    return mock_class('i2c')


@pytest.fixture
def mock_generic(mocker):
    return mocker.patch(
        'snsary.contrib.adafruit.sgp30.GenericSensor',
    )


@pytest.fixture
def sensor(mock_sgp30):
    return SGP30Sensor(mock_sgp30)


def test_init(sensor):
    assert isinstance(sensor.tracker, MaxTracker)


def test_init_no_persist(mock_sgp30):
    sensor = SGP30Sensor(mock_sgp30, persistent_baselines=False)
    assert isinstance(sensor.tracker, NullTracker)


def test_start(
    sensor,
    mock_generic,
    mock_sgp30,
):
    sensor.start()
    mock_generic.start.assert_called()
    mock_sgp30.set_iaq_baseline.assert_not_called()


def test_start_restore(
    sensor,
    mock_sgp30,
    mock_generic,
    mock_store
):
    mock_store['SGP30-tracked-values'] = {
        'baseline_TVOC': 123, 'baseline_eCO2': 456
    }

    sensor.start()

    mock_sgp30.set_iaq_baseline.assert_called_with(
        TVOC=123, eCO2=456
    )


def test_ready(sensor):
    assert not sensor.ready(elapsed_seconds=15)
    assert sensor.ready(elapsed_seconds=16)


def test_publish_batch(sensor, mock_sgp30):
    sensor.publish_batch([
        create_reading(name='temperature', value=1),
        create_reading(name='relative_humidity', value=2)
    ])

    mock_sgp30.set_iaq_relative_humidity.assert_called_with(
        celsius=1, relative_humidity=2
    )


@pytest.mark.parametrize('readings', [
    [create_reading(name='temperature')],
    [create_reading(name='relative_humidity')],
    []
])
def test_publish_batch_incomplete(sensor, mock_sgp30, readings):
    sensor.publish_batch(readings)
    mock_sgp30.set_iaq_humidity.assert_not_called()


def test_sample(sensor, mock_generic, mocker):
    mock_generic.sample.return_value = ['readings']
    mock_tracker = mocker.patch.object(sensor, 'tracker')

    assert sensor.sample() == ['readings']
    mock_tracker.update.assert_called_with(['readings'])


def test_tracked_values_changed(sensor, mock_sgp30):
    sensor.tracker.on_change(
        None, {'baseline_TVOC': 'tvoc', 'baseline_eCO2': 'eco2'}
    )

    mock_sgp30.set_iaq_baseline.assert_called_with(
        TVOC='tvoc', eCO2='eco2'
    )
