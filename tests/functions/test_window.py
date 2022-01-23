import pytest

from snsary.functions import Window
from tests.conftest import create_reading, create_sensor


@pytest.fixture
def window():
    class TestWindow(Window):
        def _aggregate(self, readings):
            return [readings[0]]

    return TestWindow(seconds=2)


def test_window(window):
    sensor1 = create_sensor()
    sensor2 = create_sensor()

    assert not window(create_reading(value=1, sensor=sensor1, timestamp_seconds=1))
    assert not window(create_reading(value=2, sensor=sensor2, timestamp_seconds=1))
    assert not window(create_reading(value=3, sensor=sensor1, timestamp_seconds=2))
    assert not window(create_reading(value=4, sensor=sensor2, timestamp_seconds=2))

    # proves multiple readings are collected
    readings = window(create_reading(value=5, sensor=sensor1, timestamp_seconds=3))
    assert len(readings) == 1
    assert readings[0].sensor == sensor1
    assert readings[0].value == 1

    assert not window(create_reading(value=5, sensor=sensor1, timestamp_seconds=4))

    # prove that multiple windows are created
    readings = window(create_reading(value=6, sensor=sensor2, timestamp_seconds=3))
    assert len(readings) == 1
    assert readings[0].sensor == sensor2
    assert readings[0].value == 2

    assert not window(create_reading(value=7, sensor=sensor2, timestamp_seconds=4))

    # proves any order of aggregations is OK
    readings = window(create_reading(value=8, sensor=sensor2, timestamp_seconds=5))
    assert len(readings) == 1
    assert readings[0].sensor == sensor2
    assert readings[0].value == 6

    # proves aggregation is by period not size
    assert not window(create_reading(value=8, sensor=sensor2, timestamp_seconds=5))
    assert not window(create_reading(value=8, sensor=sensor2, timestamp_seconds=5))
