from mics6814 import Mics6814Reading

from snsary.contrib.pimoroni import GenericSensor


def test_mics6814_i2c(mocker):
    mock_class = mocker.patch(
        'mics6814.MICS6814', autospec=True
    )

    mock_class().read_all = lambda: Mics6814Reading(
        ox=1, red=2, nh3=3, adc=4
    )

    sensor = GenericSensor.mics6814_i2c()
    assert sensor.name == 'MICS6814'
    mock_class().set_led.assert_called_with(0, 0, 0)

    readings = sorted(
        sensor.sample(timestamp_seconds=1),
        key=lambda reading: reading.name
    )

    assert len(readings) == 3
    assert 'adc' not in {r.name for r in readings}
    assert readings[0].name == 'nh3'
    assert readings[0].value == 3


def test_sample():
    sensor = GenericSensor(
        name='sensor',
        read_fn=lambda: [('name', 'value')]
    )

    readings = sensor.sample(timestamp_seconds=123)

    assert len(readings) == 1
    assert readings[0].name == 'name'
    assert readings[0].value == 'value'
    assert readings[0].sensor == sensor
    assert readings[0].timestamp == 123
