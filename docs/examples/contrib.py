#! /usr/bin/python3

import board
from adafruit_bh1750 import BH1750
from adafruit_ms8607 import MS8607
from adafruit_scd30 import SCD30
from adafruit_sgp30 import Adafruit_SGP30
from dotenv import load_dotenv

from snsary import system
from snsary.contrib.adafruit import GenericSensor as AdafruitSensor
from snsary.contrib.adafruit.sgp30 import SGP30Sensor
from snsary.contrib.awair import AwairSensor
from snsary.contrib.google import BigQueryOutput
from snsary.contrib.grafana import GraphiteOutput
from snsary.contrib.influxdb import InfluxDBOutput
from snsary.contrib.octopus import OctopusSensor
from snsary.contrib.psutil import PSUtilSensor
from snsary.contrib.pypms import PyPMSSensor
from snsary.sources import MultiSource
from snsary.streams import SimpleStream
from snsary.utils import logging, tracing

i2c = board.I2C()
load_dotenv()
logging.configure_logging()

tracing.configure(
    {
        "enabled": True,
        "monitors": [tracing.LivenessAlert.factory(), tracing.GapAlert.factory()],
        "thread_aware": True,
    }
)

# summarization is necessary to avoid exceeding BigQuery usage limits
longterm_stream = SimpleStream()
bigquery = BigQueryOutput.from_env()
longterm_stream.summarize(minutes=1).rename(append="/minute").into(bigquery)
longterm_stream.summarize(hours=1).rename(append="/hour").into(bigquery)
longterm_stream.summarize(days=1).rename(append="/day").into(bigquery)

# SGP30 uses temperature / humidity data for continuous callibration
sgp30 = SGP30Sensor(Adafruit_SGP30(i2c))

MultiSource(
    *AwairSensor.discover_from_env(),
    PyPMSSensor(sensor_name="PMSx003"),
    AdafruitSensor(SCD30(i2c)).stream.tee(sgp30),
    AdafruitSensor(BH1750(i2c)),
    AdafruitSensor(MS8607(i2c)),
    sgp30,
).stream.into(
    GraphiteOutput.from_env(),  # best for short term data + configuration
    longterm_stream,
)

MultiSource(
    OctopusSensor.electricity_from_env(),
    OctopusSensor.gas_from_env(),
).stream.into(
    InfluxDBOutput.from_env(),  # graphite can't ingest old Octopus data
    longterm_stream,
)

PSUtilSensor().stream.into(
    GraphiteOutput.from_env(),  # best for short term data + configuration
)

system.start_and_wait()
