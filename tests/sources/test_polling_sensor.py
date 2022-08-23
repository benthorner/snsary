import logging

from snsary.sources import PollingSensor


def test_tick_copes_with_generators(
    caplog,
):
    class TestSensor(PollingSensor):
        def __init__(self):
            PollingSensor.__init__(self, period_seconds=5)

        def sample(self, **kwargs):
            yield "reading"

    caplog.set_level(logging.INFO)
    TestSensor().tick()
    assert "Collected 1 readings" in caplog.text
