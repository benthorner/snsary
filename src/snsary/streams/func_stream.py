"""
Only publishes a :mod:`Reading <snsary.models.Reading>` if the specified :mod:`function <snsary.functions>` returns a :mod:`Reading <snsary.models.Reading>` for it. This could be the same reading or a different one. Nothing is published if the :mod:`function <snsary.functions>` returns ``None``.
"""
from .simple_stream import SimpleStream


class FuncStream(SimpleStream):
    def __init__(
        self,
        stream,
        function=lambda reading: reading
    ):
        SimpleStream.__init__(self)
        stream.subscribe(self)
        self.__function = function

    def publish(self, reading):
        output_reading = self.__function(reading)

        if output_reading:
            SimpleStream.publish(self, output_reading)
