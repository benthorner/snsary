from snsary.functions import WindowAverage
from tests.conftest import create_reading


def test_window_average():
    window = WindowAverage(size=3)

    assert not window(create_reading(value=1))
    assert not window(create_reading(value=5.3))

    reading = window(create_reading(value=3))
    assert reading.value == 3.1

    assert not window(create_reading())
