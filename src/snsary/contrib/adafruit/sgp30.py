"""
Wrapper for the Adafruit SGP30 sensor, inheriting from :mod:`GenericSensor <snsary.contrib.adafruit.generic>`:

    - Waits 15 seconds for the device to warm up (as per the `datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Datasheets/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf>`_).
    - Standardises the name used for logs and readings to "SGP30".

The installation and configuration is the same as the generic wrapper: ::

    # install the sensor library
    pip3 install adafruit-circuitpython-sgp30

    # create the sensor object
    import board
    i2c = board.I2C()
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

    # prepare to poll / scrape
    SGP30Sensor(sgp30)

``SGP30Sensor`` is also an :mod:`Output <snsary.outputs.output>`. The TVOC and eCO2 readings from the SGP30 sensor need to be adjusted based on the absolute humidity of the surrounding air, which `can be calculated <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Datasheets/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf>`_ from the "temperature" and "relative_humidity" in a batch of :mod:`Readings <snsary.models.reading>`: ::

    # SCD30 outputs the required readings
    GenericSensor(scd30).stream.tee(sgp30)

The required names - "tempeature" and "relative_humidity" - may not match some sensors. One way to work around this is to rename each :mod:`Reading <snsary.models.reading>` on the fly: ::

    OtherSensor.stream.filter_names('temp').rename(to='temperature').into(sgp30)
    OtherSensor.stream.filter_names('humid').rename(to='relative_humidity').into(sgp30)

``SGP30Sensor`` polls at the default period of :mod:`GenericSensor <snsary.contrib.adafruit.generic>`. The `datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Datasheets/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf>`_ says it should be 1s, but this doesn't work in practice, especially when the I2C bus is busy.
"""

from math import exp

from snsary.outputs import BatchOutput

from .generic import GenericSensor


class SGP30Sensor(GenericSensor, BatchOutput):
    def __init__(self, device):
        BatchOutput.__init__(self)
        GenericSensor.__init__(self, device)

    @property
    def name(self):
        return 'SGP30'

    def ready(self, elapsed_seconds, **kwargs):
        return elapsed_seconds > 15

    def publish_batch(self, readings):
        temperatures = self.__filter(readings, 'temperature')
        relative_humidities = self.__filter(readings, 'relative_humidity')

        if not temperatures or not relative_humidities:
            self.logger.warning('Incomplete data for self-calibration.')
            return

        H = self.__abs_humidity(
            temperatures[-1].value, relative_humidities[-1].value
        )

        self.device.set_iaq_humidity(H)

    def __abs_humidity(self, T, RH):
        numerator = ((RH / 100) * 6.112) * exp((17.62 * T) / (243.12 + T))
        denominator = 273.15 + T
        return 216.7 * (numerator / denominator)

    def __filter(self, readings, name):
        return [reading for reading in readings if reading.name == name]
