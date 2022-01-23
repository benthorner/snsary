from snsary.functions import Filter, WindowAverage, WindowSummary
from snsary.outputs import Output
from snsary.sources import Source


class Stream(Source, Output):
    def into(self, *outputs):
        for output in outputs:
            self.subscribe(output)

    def apply(self, function):
        from .func_stream import FuncStream
        return FuncStream(self, function)

    def filter_names(self, *names):
        return self.apply(Filter.names(*names))

    def average(self, **kwargs):
        """
        Returns a new stream that applies a :mod:`WindowAverage <snsary.functions.window_average>` to all :mod:`Readings <snsary.models.reading>` over a period, specified as the keyword arguments for a ``timedelta``.
        """
        return self.apply(WindowAverage(**kwargs))

    def summarize(self, **kwargs):
        """
        Returns a new stream that applies a :mod:`WindowSummary <snsary.functions.window_summary>` to all :mod:`Readings <snsary.models.reading>` over a period, specified as the keyword arguments for a ``timedelta``.
        """
        return self.apply(WindowSummary(**kwargs))
