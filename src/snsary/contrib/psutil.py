import psutil

from snsary.models import Reading
from snsary.sources import PollingSensor
from snsary.utils import scraper


class PSUtilSensor(PollingSensor):
    FUNCTIONS = {
        'cpu_times': {},
        'cpu_percent': {'interval': 1},
        'cpu_count': {},
        'cpu_stats': {},
        'getloadavg': {},
        'virtual_memory': {},
        'swap_memory': {},
        'disk_usage': {'path': '/'},
        'disk_io_counter': {},
        'net_io_counters': {},
        'sensors_temperatures': {},
        'sensors_fans': {},
        'sensors_battery': {},
    }

    def __init__(self, functions=FUNCTIONS):
        self.__functions = functions

        PollingSensor.__init__(
            self,
            name='psutil',
            period_seconds=10
        )

    def sample(self, timestamp_seconds, **kwargs):
        return [
            Reading(
                sensor=self,
                name=name,
                value=value,
                timestamp_seconds=timestamp_seconds
            )
            for fname, kwargs in self.__functions.items()
            for (name, value) in self.__sample_fn(fname, kwargs)
        ]

    def __sample_fn(self, fname, kwargs):
        if not hasattr(psutil, fname):
            self.logger.debug(f"Skipping {fname} as not available.")
            return []

        value = getattr(psutil, fname)(**kwargs)
        self.logger.debug(f'Scraping {fname} => {value}')
        return scraper.extract_from(value, prefix=fname)
