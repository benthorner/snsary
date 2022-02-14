from snsary.functions import WindowSummary
from tests.conftest import create_reading


def test_call():
    window = WindowSummary(seconds=2)

    assert not window(create_reading(value=1, timestamp=1))
    assert not window(create_reading(value=2, timestamp=2))

    readings = window(create_reading(value=3, timestamp=3))

    assert len(readings) == 4
    assert readings[0].name == 'myreading--mean'
    assert readings[0].value == 1.5
    assert readings[1].name == 'myreading--max'
    assert readings[1].value == 2
    assert readings[2].name == 'myreading--min'
    assert readings[2].value == 1
    assert readings[3].name == 'myreading--p50'
    assert readings[3].value == 1.5

    assert not window(create_reading(timestamp=4))
