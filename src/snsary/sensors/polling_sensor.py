from snsary.utils import Poller, logger

from .sensor import Sensor


class PollingSensor(Sensor, Poller):
    start = Poller.start

    def __init__(self, *, name, period_seconds):
        Sensor.__init__(self, name=name)
        Poller.__init__(self, period_seconds=period_seconds)

    def stop(self):
        Poller.stop(self)
        Sensor.stop(self)

    def _tick(self, **kwargs):
        try:
            readings = list(self.sample(**kwargs))
            logger.info(f"Collected {len(readings)} readings.")

            for reading in readings:
                self._keep(reading)
        except Exception as e:
            logger.exception(e)

    def sample(self, **kwargs):
        return []
