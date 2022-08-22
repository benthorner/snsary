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


def test_tee(stream, output):
    assert stream.tee(output) == stream
    stream.publish(create_reading())
    assert len(output.readings) == 1


def test_apply(stream, output):
    def _function(reading):
        return [create_reading(value=2)]

    stream.apply(_function).into(output)
    stream.publish(create_reading(value=1))

    assert len(output.readings) == 1
    assert output.readings[0].value == 2


def test_filter_names(stream, output):
    stream.filter_names("pass").into(output)
    stream.publish(create_reading(name="fail"))
    stream.publish(create_reading(name="pass"))

    assert len(output.readings) == 1
    assert output.readings[0].name == "pass"


def test_average(stream, output):
    stream.average(seconds=2).into(output)

    for i in range(3):
        stream.publish(create_reading(value=i + 1, timestamp=i))

    assert len(output.readings) == 1
    assert output.readings[0].value == 1.5


def test_summarize(stream, output):
    stream.summarize(seconds=2).into(output)

    for i in range(3):
        stream.publish(create_reading(value=i + 1, timestamp=i))

    assert len(output.readings) == 4
    assert output.readings[0].name == "myreading--mean"
    assert output.readings[0].value == 1.5


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({"append": "foo"}, "myreadingfoo"),
        ({"to": "bar"}, "bar"),
        ({"append": "foo", "to": "bar"}, "barfoo"),
    ],
)
def test_rename(stream, output, kwargs, expected):
    stream.rename(**kwargs).into(output)
    stream.publish(create_reading())
    assert len(output.readings) == 1
    assert output.readings[0].name == expected
