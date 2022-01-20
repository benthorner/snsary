import pytest

from snsary.functions import Window
from snsary.sources import Sensor
from tests.conftest import create_reading


@pytest.fixture
def window():
    class TestWindow(Window):
        def _aggregate(self, readings):
            return readings[0]

    return TestWindow(size=2)


def test_window(window):
    sensor1 = Sensor(name='sensor1')
    sensor2 = Sensor(name='sensor2')

    assert not window(create_reading(value=1, sensor=sensor1))
    assert not window(create_reading(value=2, sensor=sensor2))

    reading = window(create_reading(value=3, sensor=sensor1))
    assert reading.sensor == sensor1
    assert reading.value == 1

    assert not window(create_reading(value=4, sensor=sensor1))

    reading = window(create_reading(value=5, sensor=sensor2))
    assert reading.sensor == sensor2
    assert reading.value == 2

    assert not window(create_reading(value=6, sensor=sensor2))
    reading = window(create_reading(value=7, sensor=sensor2))
    assert reading.sensor == sensor2
    assert reading.value == 6
