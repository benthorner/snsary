"""
Base class for functions that aggregate :mod:`Readings <snsary.models.reading>` over a fixed, consecutive periods. A subclass should define an ``_aggregate`` method that is called each time the age of the window for a sensor / reading name pair reaches the specified period. The windows are consecutive, not moving: after a window has been aggregated a new window is created with the last :mod:`Reading <snsary.models.reading>`.
"""


class Window:
    def __init__(self, *, period=10):
        self.__period = period
        self.__windows = dict()

    def __call__(self, reading):
        key = (reading.sensor, reading.name)

        if not self.__windows.get(key, []):
            self.__windows[key] = [reading]
            return

        readings = self.__windows[key]
        start = readings[0].timestamp
        age = reading.timestamp - start

        if age >= self.__period:
            self.__windows[key] = [reading]
            return self._aggregate(readings)

        readings += [reading]
        self.__windows[key] = readings

    def aggregate(readings):
        raise NotImplementedError
