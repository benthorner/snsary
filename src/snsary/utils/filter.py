class Filter:
    def __init__(self, allow_fn=lambda _: True):
        self.__allow_fn = allow_fn

    def __call__(self, reading):
        return self.__allow_fn(reading)

    @property
    def invert(self):
        return Filter(lambda reading: not self(reading))

    @classmethod
    def sensor_name(cls, name):
        return cls(
            lambda reading: reading.sensor.name == name
        )

    @classmethod
    def names(cls, *names):
        return cls(
            lambda reading: reading.name in names
        )
