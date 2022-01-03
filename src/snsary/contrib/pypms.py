"""
An adapter for `the PyPMS library <https://github.com/avaldebe/PyPMS>`_.

Example of creating an instance::

    PyPMSSensor(sensor_name='PMSx003')
"""
import dataclasses

from pms.core import Sensor
from serial import Serial

from snsary.models import Reading
from snsary.sources import PollingSensor
from snsary.utils import logger


class PyPMSSensor(PollingSensor):
    """
    ``warm_up_seconds`` is necessary for some sensors e.g. for the PMSA003 the first two samples always `raise an InconsistentObservation exception <https://github.com/avaldebe/PyPMS/blob/04ff8edede7d780018cd00a7fcf78ffed43c0de4/src/pms/sensors/plantower/pmsx003.py#L63>`_.
    """
    def __init__(
        self,
        *,
        sensor_name,
        port='/dev/ttyS0',
        warm_up_seconds=10,
        timeout=5
    ):
        self.__sensor = Sensor[sensor_name]
        self.warm_up_seconds = warm_up_seconds

        self.__serial = Serial(
            port,
            baudrate=self.__sensor.baud,
            timeout=timeout,
        )

        PollingSensor.__init__(
            self,
            name=self.__sensor.name,
            period_seconds=10
        )

    def __cmd(self, command):
        cmd = self.__sensor.command(command)
        logger.debug(f"Sending {command} => {cmd}")
        # clear any stray inbound data
        self.__serial.reset_input_buffer()
        # no need to flush() - this can
        # cause the execution to hang
        self.__serial.write(cmd.command)
        buffer = self.__serial.read(cmd.answer_length)

        logger.debug(f"Received {buffer}")
        return buffer

    def start(self):
        self.__cmd("wake")
        buffer = self.__cmd("passive_mode")

        if not self.__sensor.check(buffer, "passive_mode"):
            raise RuntimeError("Serial port not connected.")

        PollingSensor.start(self)

    def stop(self):
        PollingSensor.stop(self)

        try:
            self.__cmd("sleep")
            self.__serial.close()
        except Exception as e:
            logger.exception(e)

    def sample(self, timestamp_seconds, elapsed_seconds, **kwargs):
        if elapsed_seconds < self.warm_up_seconds:
            logger.info("Still warming up, no data yet.")
            return []

        buffer = self.__cmd("passive_read")
        obs = self.__sensor.decode(buffer)

        return [
            Reading(
                sensor=self,
                name=key,
                value=value,
                timestamp_seconds=timestamp_seconds
            )
            for key, value in dataclasses.asdict(obs).items()
            if key not in ('time')
        ]
