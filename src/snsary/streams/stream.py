from snsary.outputs import Output
from snsary.sources import Source
from snsary.utils import Filter


class Stream(Source, Output):
    def into(self, *outputs):
        for output in outputs:
            self.subscribe(output)

    def filter(self, filter):
        from .filter_stream import FilterStream
        return FilterStream(self, filter)

    def filter_names(self, *names):
        return self.filter(Filter.names(*names))
