"""
Base class for functions that aggregate :mod:`Readings <snsary.models.reading>` over a fixed, consecutive windows. A subclass should define an ``_aggregate`` method that is called each time the window for a sensor / reading name pair exceeds the specified size. The windows are consecutive, not moving: after a window has been aggregated a new window is created.
"""


class Window:
    def __init__(self, *, size=3):
        self.__size = size
        self.__windows = dict()

    def __call__(self, reading):
        key = (reading.sensor, reading.name)

        if key not in self.__windows:
            self.__windows[key] = []

        readings = self.__windows[key] + [reading]

        if len(readings) >= self.__size:
            self.__windows[key] = []
            return self._aggregate(readings)

        self.__windows[key] = readings

    def aggregate(readings):
        raise NotImplementedError
