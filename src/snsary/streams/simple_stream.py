from .stream import Stream


class SimpleStream(Stream):
    def __init__(self):
        self.__outputs = []

    def publish(self, reading):
        for output in self.__outputs:
            output.publish(reading)

    def subscribe(self, output):
        self.__outputs += [output]
