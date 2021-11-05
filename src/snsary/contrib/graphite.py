import json
import platform

import requests

from snsary.outputs import BatchOutput
from snsary.utils import logger


class GraphiteOutput(BatchOutput):
    def __init__(self, *, url, prefix=None):
        BatchOutput.__init__(self)
        self.__url = url
        self.__prefix = prefix or platform.node()

    def send_batch(self, readings):
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
