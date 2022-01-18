import pytest
from retry import retry as retrier

from snsary.models import Reading
from snsary.sources import Sensor


def retry(fn):
    # logger=None stops failure logs causing a false positive
    retrier(tries=5, delay=0.5, logger=None)(fn)()


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
