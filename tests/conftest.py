import pytest

from snsary.models import Reading
from snsary.sources import Sensor


@pytest.fixture
def reading():
    return create_reading()


def create_reading(
    *,
    sensor=Sensor(name='mysensor'),
    timestamp_seconds=123,
    value=123,
    name='myreading'
):
    return Reading(
        sensor=sensor,
        timestamp_seconds=timestamp_seconds,
        value=value,
        name=name
    )
