from datetime import timedelta

import pyrfc3339
import requests

from snsary.models import Reading
from snsary.sensors import PollingSensor
from snsary.utils import logger

ONE_DAY = 24 * 60 * 60


class OctopusSensor(PollingSensor):
    CONSUMPTION_URL = "https://api.octopus.energy/v1/electricity-meter-points/{mpan}/meters/{serial_number}/consumption/?period_from={period_from}&order_by=period"

    def __init__(self, *, mpan, serial_number, token):
        PollingSensor.__init__(
            self,
            name='octopus',
            period_seconds=30 * 60  # 30 mins
        )

        self.__token = token
        self.__mpan = mpan
        self.__serial_number = serial_number

    def sample(self, now, **kwargs):
        start = now - timedelta(days=1)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)

        url = self.CONSUMPTION_URL.format(
            mpan=self.__mpan,
            serial_number=self.__serial_number,
            period_from=start.isoformat(),
        )

        logger.debug('Request {url}')
        response = requests.get(
            url, auth=(self.__token, '')
        )
        response.raise_for_status()
        samples = response.json()["results"]
        logger.debug(f'Response {samples}')

        return [
            self.__sample_reading(sample) for sample in samples
        ]

    def __sample_reading(self, sample):
        sample_timestamp = int(
            pyrfc3339.parse(sample["interval_end"]).timestamp()
        )

        return Reading(
            sensor=self,
            name='consumption',
            timestamp_seconds=sample_timestamp,
            value=sample["consumption"],
        )
