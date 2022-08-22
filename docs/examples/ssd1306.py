#! /usr/bin/python3

"""
Shows a count of readings published.

Prerequisites: ::

    pip3 install adafruit-circuitpython-ssd1306

    wget https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_framebuf/main/examples/font5x8.bin
"""

import adafruit_ssd1306
import board

from snsary import system
from snsary.outputs import Output
from snsary.sources import MockSensor
from snsary.utils import Service, configure_logging


class OLEDOutput(Output, Service):
    def __init__(self, i2c):
        Service.__init__(self)

        self.__display = adafruit_ssd1306.SSD1306_I2C(
            width=128, height=32, i2c=i2c, addr=0x3C
        )

        self.__count = 0

    def start(self):
        self.__display.poweron()

    def stop(self):
        self.__display.poweroff()

    def publish(self, reading):
        self.__count += 1
        self.__display.fill(0)
        self.__display.text(f"Sent {self.__count} readings.", 0, 0, color=1)
        self.__display.show()


i2c = board.I2C()
MockSensor().subscribe(OLEDOutput(i2c))
configure_logging()
system.start_and_wait()
