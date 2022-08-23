import logging

from snsary.outputs import MockOutput
from snsary.streams import SimpleStream
from tests.conftest import retry


def test_publish_exception(caplog):
    stream = SimpleStream()
    stream.subscribe(MockOutput(fail=True))
    stream.subscribe(MockOutput(index=1))

    caplog.set_level(logging.INFO)
    stream.publish("reading")

    def assertions():
        assert "ERROR - [snsary.mockoutput-0] problem-1" in caplog.text
        assert "INFO - [snsary.mockoutput-1] Reading" in caplog.text

    retry(assertions)
