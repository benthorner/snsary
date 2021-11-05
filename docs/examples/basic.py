#! /usr/bin/python3

import logging
import sys

from snsary import App
from snsary.outputs import MockOutput
from snsary.sensors import MockSensor

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s"
)

app = App(
    sensors=[
        MockSensor(),
    ],
    outputs=[
        MockOutput(),
    ]
)

app.handle_signals()
app.start()
app.wait()
