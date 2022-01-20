from snsary.functions import Filter, WindowAverage
from snsary.outputs import Output
from snsary.sources import Source


class Stream(Source, Output):
    def into(self, *outputs):
        for output in outputs:
            self.subscribe(output)

    def apply(self, function):
        from .func_stream import FuncStream
        return FuncStream(self, function)

    def filter(self, filter):
        def _filter(reading):
            if filter(reading):
                return reading

        return self.apply(_filter)

    def filter_names(self, *names):
        return self.apply(Filter.names(*names))

    def average(self, size=3):
        return self.apply(WindowAverage(size=size))
