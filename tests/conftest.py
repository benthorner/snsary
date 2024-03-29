import pytest
from retry import retry as retrier

from snsary.models import Reading
from snsary.sources import Sensor
from snsary.utils import storage


def retry(fn):
    # logger=None stops failure logs causing a false positive
    retrier(tries=5, delay=0.5, logger=None)(fn)()


@pytest.fixture
def reading():
    return create_reading()


@pytest.fixture
def mock_store():
    yield storage.get_storage()
    storage.get_storage().clear()


@pytest.fixture
def sensor():
    class FakeSensor(Sensor):
        @property
        def name(self):
            return "mysensor"

    return FakeSensor()


def create_reading(
    *,
    sensor_name="mysensor",
    timestamp=1650745546,  # 2022-04-23T21:25:46+01:00
    value=123,
    name="myreading"
):
    return Reading(
        sensor_name=sensor_name,
        timestamp=timestamp,
        value=value,
        name=name,
    )
