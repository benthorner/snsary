import adafruit_bh1750
import board

from snsary import system
from snsary.contrib.adafruit import AdafruitSensor
from snsary.outputs import MockOutput
from snsary.utils import configure_logging

i2c = board.I2C()
bh1750 = adafruit_bh1750.BH1750(i2c)

AdafruitSensor(bh1750).subscribe(MockOutput())
configure_logging()
system.start_and_wait()
