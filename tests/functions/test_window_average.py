from snsary.functions import WindowAverage
from tests.conftest import create_reading


def test_call():
    window = WindowAverage(seconds=2)

    assert not window(create_reading(value=1, timestamp_seconds=1))
    assert not window(create_reading(value=2, timestamp_seconds=2))

    readings = window(create_reading(value=3, timestamp_seconds=3))
    assert len(readings) == 1
    assert readings[0].value == 1.5

    assert not window(create_reading(timestamp_seconds=4))
