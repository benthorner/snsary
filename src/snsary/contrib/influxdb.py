import os
import platform

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from snsary.outputs import BatchOutput
from snsary.utils import logger


class InfluxDBOutput(BatchOutput):
    @classmethod
    def from_env(cls):
        return cls(
            url=os.environ['INFLUXDB_URL'],
            token=os.environ['INFLUXDB_TOKEN'],
            org=os.environ['INFLUXDB_ORG'],
            bucket=os.environ['INFLUXDB_BUCKET']
        )

    def __init__(self, *, url, token, org, bucket):
        BatchOutput.__init__(self)
        client = InfluxDBClient(url=url, token=token, org=org)
        self.__bucket = bucket
        self.__write_api = client.write_api(write_options=SYNCHRONOUS)

    def publish_batch(self, readings):
        points = [
            Point(reading.name)
            .tag('sensor', reading.sensor.name)
            .tag('host', platform.node())
            .field('value', reading.value)
            .time(reading.timestamp, write_precision='s')
            for reading in readings
        ]

        logger.debug('Sending ' + str(list(
            point.to_line_protocol() for point in points
        )))

        self.__write_api.write(
            bucket=self.__bucket, record=points
        )
