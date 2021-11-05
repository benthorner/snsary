from datetime import timedelta

import pyrfc3339
import requests

from snsary.models import Reading
from snsary.sensors import PollingSensor
from snsary.utils import logger


class AwairSensor(PollingSensor):
    DEVICES_URL = "https://developer-apis.awair.is/v1/users/self/devices"
    DATA_URL = "https://developer-apis.awair.is/v1/users/self/devices/{deviceType}/{deviceId}/air-data/raw?from={from}&desc=False"
    PERIOD = 5 * 60  # 5 mins

    @classmethod
    def discover(cls, *, token):
        logger.debug(f'Request {cls.DEVICES_URL}')
        response = requests.get(
            cls.DEVICES_URL, headers={'Authorization': f'Bearer {token}'}
        )
        response.raise_for_status()
        devices = response.json()["devices"]

        logger.info(f"Discovered {len(devices)} Awair devices.")
        logger.debug(f'Discovered {devices}')

        return [
            AwairSensor(
                device_type=device['deviceType'],
                device_id=device['deviceId'],
                token=token
            )
            for device in devices
        ]

    def __init__(self, *, device_type, device_id, token):
        PollingSensor.__init__(
            self,
            name=f'{device_type}-{device_id}',
            period_seconds=self.PERIOD
        )

        self.__token = token
        self.__device_type = device_type
        self.__device_id = device_id

    def sample(self, now, **kwargs):
        # subtract double period in case of delayed readings
        sample_start = now - timedelta(seconds=self.PERIOD * 2)

        url = self.DATA_URL.format(**{
            'deviceType': self.__device_type,
            'deviceId': self.__device_id,
            'from': sample_start.isoformat()
        })

        logger.debug(f'Request {url}')
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {self.__token}'}
        )
        response.raise_for_status()
        samples = response.json()["data"]
        logger.debug('Response {samples}')

        return [
            reading for sample in samples
            for reading in self.__sample_readings(sample)
        ]

    def __sample_readings(self, sample):
        sample_timestamp = int(
            pyrfc3339.parse(sample["timestamp"]).timestamp()
        )

        return (
            Reading(
                sensor=self,
                name=sensor["comp"],
                timestamp_seconds=sample_timestamp,
                value=sensor["value"]
            )
            for sensor in sample["sensors"]
        )
