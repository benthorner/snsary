"""
Outputs raw (unaveraged) data from all sensors of a specified device every 5 minutes. The long period is necessary due to the severe rate limiting Awair have on `their API <https://docs.developer.getawair.com/#local-api>`_.

Calling ``.discover()`` will auto-discover and return a list of AwairSensors associated with an account, which is more convenient than having to manually find and specify the details of each device. You can also call ``.discover_from_env``, which expects:

- AWAIR_TOKEN
"""

import os
from datetime import timedelta

import pyrfc3339
import requests

from snsary.models import Reading
from snsary.sources import PollingSensor
from snsary.utils import get_logger


class AwairSensor(PollingSensor):
    DEVICES_URL = "https://developer-apis.awair.is/v1/users/self/devices"
    DATA_URL = "https://developer-apis.awair.is/v1/users/self/devices/{deviceType}/{deviceId}/air-data/raw?from={from}&desc=False"
    PERIOD = 5 * 60  # 5 mins

    @classmethod
    def discover_from_env(cls):
        return cls.discover(
            token=os.environ['AWAIR_TOKEN']
        )

    @classmethod
    def discover(cls, *, token):
        get_logger().debug(f'Request {cls.DEVICES_URL}')
        response = requests.get(
            cls.DEVICES_URL, headers={'Authorization': f'Bearer {token}'}
        )
        response.raise_for_status()
        devices = response.json()["devices"]

        get_logger().info(f"Discovered {len(devices)} Awair devices.")
        get_logger().debug(f'Discovered {devices}')

        return [
            AwairSensor(
                device_type=device['deviceType'],
                device_id=device['deviceId'],
                token=token
            )
            for device in devices
        ]

    def __init__(self, *, device_type, device_id, token):
        PollingSensor.__init__(self, period_seconds=self.PERIOD)
        self.__token = token
        self.__device_type = device_type
        self.__device_id = device_id

    @property
    def name(self):
        return f'{self.__device_type}-{self.__device_id}'

    def sample(self, now, **kwargs):
        # subtract double period in case of delayed readings
        sample_start = now - timedelta(seconds=self.PERIOD * 2)

        url = self.DATA_URL.format(**{
            'deviceType': self.__device_type,
            'deviceId': self.__device_id,
            'from': sample_start.isoformat()
        })

        self.logger.debug(f'Request {url}')
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {self.__token}'}
        )
        response.raise_for_status()
        samples = response.json()["data"]
        self.logger.debug('Response {samples}')

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
                sensor_name=self.name,
                name=sensor["comp"],
                timestamp=sample_timestamp,
                value=sensor["value"]
            )
            for sensor in sample["sensors"]
        )
