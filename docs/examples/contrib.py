#! /usr/bin/python3

import logging
import os
import sys

import adafruit_bh1750
import adafruit_scd30
import board
from dotenv import load_dotenv

from snsary import App
from snsary.contrib.adafruit import AdafruitSensor
from snsary.contrib.awair import AwairSensor
from snsary.contrib.graphite import GraphiteOutput
from snsary.contrib.influxdb import InfluxDBOutput
from snsary.contrib.octopus import OctopusSensor
from snsary.contrib.psutil import PSUtilSensor
from snsary.contrib.pypms import PyPMSSensor
from snsary.utils import Filter

i2c = board.I2C()
bh1750 = adafruit_bh1750.BH1750(i2c)
scd30 = adafruit_scd30.SCD30(i2c)
scd30.temperature_offset = 4

load_dotenv()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s"
)

app = App(
    sensors=[
        PSUtilSensor(),
        OctopusSensor(
            mpan=os.environ['OCTOPUS_MPAN'],
            serial_number=os.environ['OCTOPUS_SERIAL'],
            token=os.environ['OCTOPUS_TOKEN'],
        ),
        *AwairSensor.discover(token=os.environ['AWAIR_TOKEN']),
        PyPMSSensor(sensor_name='PMSx003', port='/dev/ttyS0'),
        AdafruitSensor(scd30),
        AdafruitSensor(bh1750),
    ],
    outputs=[
        GraphiteOutput(url=os.environ['GRAPHITE_URL']),
        InfluxDBOutput(
            url=os.environ['INFLUX_URL'],
            token=os.environ['INFLUX_TOKEN'],
            org=os.environ['INFLUX_ORG'],
            bucket=os.environ['INFLUX_BUCKET']
        ).filter(
            Filter.names(
                'pm10', 'pm25', 'temp', 'humid', 'co2', 'CO2',
                'voc', 'temperature', 'relative_humidity', 'lux',
                'consumption'
            )
        )
    ]
)

app.handle_signals()
app.start()
app.wait()
