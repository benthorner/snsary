#! /usr/bin/python3

import adafruit_bh1750
import adafruit_scd30
import board
from dotenv import load_dotenv

from snsary import system
from snsary.contrib.adafruit import AdafruitSensor
from snsary.contrib.awair import AwairSensor
from snsary.contrib.grafana import GraphiteOutput
from snsary.contrib.influxdb import InfluxDBOutput
from snsary.contrib.octopus import OctopusSensor
from snsary.contrib.psutil import PSUtilSensor
from snsary.contrib.pypms import PyPMSSensor
from snsary.sources import MultiSource
from snsary.utils import configure_logging

i2c = board.I2C()
bh1750 = adafruit_bh1750.BH1750(i2c)
scd30 = adafruit_scd30.SCD30(i2c)
scd30.temperature_offset = 4

load_dotenv()
configure_logging()

MultiSource(
    OctopusSensor.from_env(),
    *AwairSensor.discover_from_env(),
    PyPMSSensor(sensor_name='PMSx003').stream.filter_names('pm10', 'pm25'),
    AdafruitSensor(scd30).stream.filter_names('CO2', 'temperature', 'relative_humidity'),
    AdafruitSensor(bh1750).stream.filter_names('lux')
).stream.into(
    GraphiteOutput.from_env(),
    InfluxDBOutput.from_env()
)

PSUtilSensor().stream.into(
    GraphiteOutput.from_env()
)

system.start_and_wait()
