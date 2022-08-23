from snsary.functions import WindowAverage
from tests.conftest import create_reading


def test_aggregate():
    window = WindowAverage(seconds=2)

    readings = window.aggregate(
        [
            create_reading(value=1, timestamp=1),
            create_reading(value=2, timestamp=2),
        ]
    )

    assert len(readings) == 1
    assert readings[0].value == 1.5
