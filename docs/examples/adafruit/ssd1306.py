#! /usr/bin/python3

import logging
import sys

import adafruit_ssd1306
import busio
from board import SCL, SDA

from snsary import App
from snsary.outputs import Output
from snsary.sensors import MockSensor


class OLEDOutput(Output):
    def __init__(self, i2c):
        self.__display = adafruit_ssd1306.SSD1306_I2C(
            width=128, height=32, i2c=i2c, addr=0x3C
        )

        self.__count = 0
        self.__display.poweron()

    def send(self, reading):
        self.__count += 1
        self.__display.fill(0)
        self.__display.text(f'Sent {self.__count} readings.', 0, 0, color=1)
        self.__display.show()

    def flush(self):
        self.__display.poweroff()


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s"
)

i2c = busio.I2C(SCL, SDA)

app = App(
    sensors=[MockSensor()],
    outputs=[OLEDOutput(i2c)]
)

app.handle_signals()
app.start()
app.wait()
