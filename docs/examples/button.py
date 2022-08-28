#! /usr/bin/python3

"""
Prints whether a button at GPIO17 is pressed:

- Not pressed = True / 1
- Pressed = False / 0

Prerequisites: ::

    pip3 install Adafruit-Blinka
"""


import board
import digitalio

from snsary import system
from snsary.models import Reading
from snsary.outputs import MockOutput
from snsary.sources import PollingSensor
from snsary.utils import logging


class ButtonSensor(PollingSensor):
    def __init__(self):
        PollingSensor.__init__(self, period_seconds=10)
        self.__button = digitalio.DigitalInOut(board.D17)
        self.__button.direction = digitalio.Direction.INPUT

    def sample(self, timestamp, **kwargs):
        return [
            Reading(
                sensor_name=self.name,
                name="pressed",
                timestamp=timestamp,
                value=self.__button.value,
            )
        ]


ButtonSensor().subscribe(MockOutput())
logging.configure_logging()
system.start_and_wait()
