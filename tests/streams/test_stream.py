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


def test_apply(stream, output):
    def _function(reading):
        return create_reading(value=2)

    stream.apply(_function).into(output)
    stream.publish(create_reading(value=1))

    assert len(output.readings) == 1
    assert output.readings[0].value == 2


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


def test_average(stream, output):
    stream.average(period=2).into(output)

    for i in range(3):
        stream.publish(create_reading(
            value=i+1, timestamp_seconds=i
        ))

    assert len(output.readings) == 1
    assert output.readings[0].value == 1.5
