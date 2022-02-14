import pytest

from snsary.functions import Window
from tests.conftest import create_reading


@pytest.fixture
def window():
    class TestWindow(Window):
        def aggregate(self, readings):
            return [readings[0]]

    return TestWindow(seconds=2)


def test_call(window):
    assert not window(create_reading(value=1, sensor_name='sensor1', timestamp=1))
    assert not window(create_reading(value=2, sensor_name='sensor2', timestamp=1))
    assert not window(create_reading(value=3, sensor_name='sensor1', timestamp=2))
    assert not window(create_reading(value=4, sensor_name='sensor2', timestamp=2))

    # proves multiple readings are collected
    readings = window(create_reading(value=5, sensor_name='sensor1', timestamp=3))
    assert len(readings) == 1
    assert readings[0].sensor_name == 'sensor1'
    assert readings[0].value == 1

    assert not window(create_reading(value=5, sensor_name='sensor1', timestamp=4))

    # prove that multiple windows are created
    readings = window(create_reading(value=6, sensor_name='sensor2', timestamp=3))
    assert len(readings) == 1
    assert readings[0].sensor_name == 'sensor2'
    assert readings[0].value == 2

    assert not window(create_reading(value=7, sensor_name='sensor2', timestamp=4))

    # proves any order of aggregations is OK
    readings = window(create_reading(value=8, sensor_name='sensor2', timestamp=5))
    assert len(readings) == 1
    assert readings[0].sensor_name == 'sensor2'
    assert readings[0].value == 6

    # proves aggregation is by period not size
    assert not window(create_reading(value=8, sensor_name='sensor2', timestamp=5))
    assert not window(create_reading(value=8, sensor_name='sensor2', timestamp=5))
