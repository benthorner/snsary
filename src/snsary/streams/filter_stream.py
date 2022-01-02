"""
Only publishes a :mod:`Reading <snsary.models.reading>` if it returns ``True`` when passed through a *filter function*.
"""

from .simple_stream import SimpleStream


class FilterStream(SimpleStream):
    def __init__(self, stream, filter):
        SimpleStream.__init__(self)
        self.__filter = filter
        stream.subscribe(self)

    def publish(self, reading):
        if self.__filter(reading):
            SimpleStream.publish(self, reading)
