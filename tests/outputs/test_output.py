import pytest

from snsary.outputs import Output
from snsary.utils import Filter


@pytest.fixture
def output():
    class FakeOutput(Output):
        def send(self, reading):
            self.sent = True

    return FakeOutput()


def test_filter(output):
    output.sent = False
    output.filter(Filter()).send('reading')
    assert output.sent

    output.sent = False
    output.filter(Filter().invert).send('reading')
    assert not output.sent
