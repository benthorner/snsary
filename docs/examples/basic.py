#! /usr/bin/python3

from snsary import system
from snsary.outputs import MockOutput
from snsary.sources import MockSensor
from snsary.utils import logging

MockSensor().subscribe(MockOutput())
logging.configure_logging()
system.start_and_wait()
