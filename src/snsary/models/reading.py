from datetime import datetime


class Reading:
    def __init__(self, *, sensor, name, timestamp_seconds, value):
        self.__sensor = sensor
        self.__name = name
        self.__value = value
        self.__timestamp = timestamp_seconds

    @property
    def sensor(self):
        return self.__sensor

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def datetime(self):
        return datetime.utcfromtimestamp(self.timestamp)

    def __str__(self):
        return f'<{self.name} {self.timestamp} {self.value}>'
