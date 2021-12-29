from dotenv import load_dotenv

from snsary import system
from snsary.contrib.influxdb import InfluxDBOutput
from snsary.sources import MockSensor
from snsary.utils import configure_logging

load_dotenv()
configure_logging()

MockSensor().subscribe(
    # expects:
    #
    #  - INFLUXDB_URL
    #  - INFLUXDB_TOKEN
    #  - INFLUXDB_ORG
    #  - INFLUXDB_BUCKET
    #
    InfluxDBOutput.from_env()
)

system.start_and_wait()
