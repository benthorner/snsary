from snsary.functions import WindowAverage
from tests.conftest import create_reading


def test_window_average():
    window = WindowAverage(period=2)

    assert not window(create_reading(value=1, timestamp_seconds=1))
    assert not window(create_reading(value=2, timestamp_seconds=2))

    reading = window(create_reading(value=3, timestamp_seconds=3))
    assert reading.value == 1.5

    assert not window(create_reading(timestamp_seconds=4))
