import pytest

from snsary.outputs import Output
from snsary.streams import SimpleStream
from tests.conftest import create_reading


@pytest.fixture
def stream():
    return SimpleStream()


@pytest.fixture
def output():
    class FakeOutput(Output):
        def __init__(self):
            self.readings = []

        def publish(self, reading):
            self.readings += [reading]

    return FakeOutput()


def test_filter(stream, output):
    stream.filter(
        lambda reading: reading.name == 'pass'
    ).into(output)

    stream.publish(create_reading(name='fail'))
    stream.publish(create_reading(name='pass'))

    assert len(output.readings) == 1
    assert output.readings[0].name == 'pass'


def test_filter_names(stream, output):
    stream.filter_names('pass').into(output)
    stream.publish(create_reading(name='fail'))
    stream.publish(create_reading(name='pass'))

    assert len(output.readings) == 1
    assert output.readings[0].name == 'pass'
