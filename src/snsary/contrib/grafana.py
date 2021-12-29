import json
import os
import platform

import requests

from snsary.outputs import BatchOutput
from snsary.utils import logger


class GraphiteOutput(BatchOutput):
    @classmethod
    def from_env(cls):
        return cls(
            url=os.environ['GRAPHITE_URL'],
            prefix=platform.node()
        )

    def __init__(self, *, url, prefix):
        BatchOutput.__init__(self)
        self.__url = url
        self.__prefix = prefix

    def publish_batch(self, readings):
        data = self.__format(readings)
        logger.debug(f"Sending {data}")

        response = requests.post(
            self.__url,
            data=data,
            headers={'Content-Type': 'application/json'},
        )

        logger.debug(response.text)
        response.raise_for_status()

    def __format(self, readings):
        return json.dumps([
            {
                'name': f'{self.__prefix}.{reading.sensor.name}.{reading.name}',
                'value': reading.value,
                'time': reading.timestamp,
                'interval': 1
            } for reading in readings
        ])
