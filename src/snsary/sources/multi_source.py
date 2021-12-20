from .source import Source


class MultiSource(Source):
    def __init__(self, *sources):
        from snsary.streams import AsyncStream
        self.__stream = AsyncStream()

        for source in sources:
            source.subscribe(self.__stream)

    def subscribe(self, output):
        self.stream.subscribe(output)

    @property
    def stream(self):
        return self.__stream
