"""
A :mod:`Stream <snsary.streams.stream>` is an :mod:`Output <snsary.outputs.output>` and a :mod:`Source <snsary.sources.source>`. Being an :mod:`Output <snsary.outputs.output>` means :mod:`Sources <snsary.sources.source>` can feed into it. Being a :mod:`Source <snsary.sources.source>` means it can feed :mod:`Outputs <snsary.outputs.output>`. All :mod:`Sensors <snsary.sources.sensor>` expose a ``stream`` of their :mod:`Readings <snsary.models.reading>` e.g. ``MockSensor().stream`` returns an :mod:`AsyncStream <snsary.streams.async_stream>`.

Any Stream can be wrapped in a filter e.g. ::

    stream.filter(lambda r: True).subscribe(MockOutput())

    stream.filter_names('a', 'b', 'c').subscribe(MockOutput())

To help make filter functions there is a :mod:`Filter <snsary.functions.filter>` class. Streams also make it easy to subscribe multiple :mod:`Outputs <snsary.outputs.output>` by passing them all to ``.into()``: ::

    # same as calling "subscribe" for each
    stream.into(MockOutput(), MockOutput())

A stream can actually be used to ``apply`` any :mod:`function <snsary.functions>` to the readings that pass through it. For example, to average the distinct readings received in a window: ::

    # output an average every 3 readings
    # for each distinct sensor / reading name
    stream.average(size=3).into(MockOutput())

``average`` is just a convenience method for ``apply``.
"""


from .async_stream import AsyncStream
from .simple_stream import SimpleStream
from .stream import Stream

__all__ = [
    "SimpleStream",
    "AsyncStream",
    "Stream"
]
