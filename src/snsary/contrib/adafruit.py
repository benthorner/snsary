"""
Wrapper for most Adafruit sensor objects, which usually have one or more properties to retrieve the current values of the sensor. GenericSensor polls a given sensor object and publishes the latest value of each property as a :mod:`Reading <snsary.models.reading>`.

Most Adafruit sensors come with a driver written for CircuitPython, which can be used in pure Python via `the Adafruit Blinka library <https://github.com/adafruit/Adafruit_Blinka>`_. You will need to separately install the CircuitPython library for each sensor you want to scrape. For each sensor, you will then need to manually create and configure an instance of GenericSensor.

Example for `the BH1750 light sensor <https://github.com/adafruit/Adafruit_CircuitPython_BH1750>`_: ::

    # install the sensor library
    pip3 install adafruit-circuitpython-bh1750

    # create the sensor object
    import board
    i2c = board.I2C()
    bh1750 = adafruit_bh1750.BH1750(i2c)

    # prepare to poll / scrape
    GenericSensor(bh1750)

Although GenericSensor will only scrape numerical values, these aren't always wanted. For example, `the Adafruit SCD30 sensor class exposes an unwanted self_calibration_enabled property <https://github.com/adafruit/Adafruit_CircuitPython_SCD30/blob/b3d9bd141ae86ec4f871ae42a35d208003672c02/adafruit_scd30.py#L130>`_. You can use :mod:`Stream <snsary.streams.stream>` filters to clean up the output e.g.::

    GenericSensor(scd30).stream.filter_names('CO2', 'temperature', 'relative_humidity')

Warning: the Adafruit I2C library does have `a locking feature <https://github.com/adafruit/Adafruit_Blinka/blob/fa80f7d2ef51b0aea92196e96c3584512d30e64d/src/adafruit_blinka/__init__.py#L61-L66>`_, but it's not thread-safe. This means it's possible for multiple sensors to conflict if they poll for data around the exact same time.
"""

from snsary.models import Reading
from snsary.sources import PollingSensor
from snsary.utils import scraper


class GenericSensor(PollingSensor):
    def __init__(
        self,
        device,
        ready_fn=lambda device: True,
        period_seconds=10
    ):
        PollingSensor.__init__(
            self,
            name=type(device).__name__,
            period_seconds=period_seconds
        )

        self.__ready_fn = ready_fn
        self.__device = device
        self.__scraper = scraper.for_class(type(device))

    def sample(self, timestamp_seconds, **kwargs):
        if not self.__ready_fn(self.__device):
            raise RuntimeError('Device has no data to read.')

        return [
            Reading(
                sensor=self,
                name=name,
                value=value,
                timestamp_seconds=timestamp_seconds
            )
            for (name, value) in self.__scraper(self.__device)
        ]
