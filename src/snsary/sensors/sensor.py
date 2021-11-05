from queue import Queue

from snsary.models import EOF


class Sensor:
    def __init__(self, *, name):
        self.__name = name
        self.__queue = Queue()

    @property
    def name(self):
        return self.__name

    def start(self):
        pass

    def stop(self):
        self.__queue.put(EOF())

    def _keep(self, reading):
        self.__queue.put(reading)

    def read(self):
        return self.__queue.get()

    def filter(self, filter):
        from .filter_sensor import FilterSensor
        return FilterSensor(self, filter)

    def __str__(self):
        return f'{type(self).__name__.lower()}-{id(self)}'
