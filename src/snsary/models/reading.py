from datetime import datetime


class Reading:
    def __init__(self, *, sensor_name, name, timestamp, value):
        self.__sensor_name = sensor_name
        self.__name = name
        self.__value = value
        self.__timestamp = timestamp

    @property
    def sensor_name(self):
        return self.__sensor_name

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
