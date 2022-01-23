"""
Base class for functions that aggregate :mod:`Readings <snsary.models.reading>` over fixed, consecutive periods, specified as the keyword arguments for a ``timedelta`` (seconds, minutes, etc.).

A subclass should define an ``_aggregate`` method that is called each time the age of the window for a sensor / reading name pair reaches the specified period.

The windows are consecutive, not moving: after a window has been aggregated a new window is started using the :mod:`Reading <snsary.models.reading>` that triggered the previous window to close.
"""


from datetime import timedelta

from .function import Function


class Window(Function):
    def __init__(self, **kwargs):
        self.__period = timedelta(**kwargs).total_seconds()
        self.__windows = dict()

    def __call__(self, reading):
        key = (reading.sensor, reading.name)

        if not self.__windows.get(key, []):
            self.logger.debug(f"Starting window for {key}.")
            self.__windows[key] = [reading]
            return []

        readings = self.__windows[key]
        start = readings[0].timestamp
        age = reading.timestamp - start

        if age >= self.__period:
            self.logger.debug(f"Closing window for {key}.")
            self.__windows[key] = [reading]
            return self._aggregate(readings)

        readings += [reading]
        self.__windows[key] = readings
        return []

    def aggregate(readings):
        raise NotImplementedError()
