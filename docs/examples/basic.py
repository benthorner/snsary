#! /usr/bin/python3

from snsary import system
from snsary.outputs import MockOutput
from snsary.sources import MockSensor
from snsary.utils import configure_logging

MockSensor().subscribe(MockOutput())
configure_logging()
system.start_and_wait()
