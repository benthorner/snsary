from .source import Source


class Sensor(Source):
    def __init__(self, *, name):
        self.__name = name

        from snsary.streams import AsyncStream
        self.__stream = AsyncStream()

    @property
    def stream(self):
        return self.__stream

    @property
    def name(self):
        return self.__name

    def subscribe(self, output):
        self.stream.subscribe(output)
