from snsary.models import Reading
from snsary.sensors import PollingSensor
from snsary.utils import property_scraper


class AdafruitSensor(PollingSensor):
    def __init__(
        self,
        device,
        ready_fn=lambda device: True,
        period_seconds=10
    ):
        PollingSensor.__init__(
            self,
            name=type(device).__name__,
            period_seconds=period_seconds
        )

        self.__ready_fn = ready_fn
        self.__device = device
        self.__scraper = property_scraper(type(device))

    def sample(self, timestamp_seconds, **kwargs):
        if not self.__ready_fn(self.__device):
            raise RuntimeError('Device has no data to read.')

        return [
            Reading(
                sensor=self,
                name=name,
                value=value,
                timestamp_seconds=timestamp_seconds
            )
            for (name, value) in self.__scraper(self.__device)
        ]
