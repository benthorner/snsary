"""
A :mod:`Stream <snsary.streams.stream>` is an :mod:`Output <snsary.outputs.output>` and a :mod:`Source <snsary.sources.source>`. Being an :mod:`Output <snsary.outputs.output>` means :mod:`Sources <snsary.sources.source>` can feed into it. Being a :mod:`Source <snsary.sources.source>` means it can feed :mod:`Outputs <snsary.outputs.output>`. All :mod:`Sensors <snsary.sources.sensor>` expose a ``stream`` of their :mod:`Readings <snsary.models.reading>` e.g. ``MockSensor().stream`` returns an :mod:`AsyncStream <snsary.streams.async_stream>`.

Any Stream can be wrapped in a filter e.g. ::

    stream.filter(lambda r: True).subscribe(MockOutput())

    stream.filter_names('a', 'b', 'c').subscribe(MockOutput())

To help make filter functions there is a :mod:`Filter <snsary.utils.filter>` utility. Streams also make it easy to subscribe multiple :mod:`Outputs <snsary.outputs.output>` by passing them all to ``.into()``: ::

    # same as calling "subscribe" for each
    stream.into(MockOutput(), MockOutput())
"""


from .async_stream import AsyncStream
from .simple_stream import SimpleStream
from .stream import Stream

__all__ = [
    "SimpleStream",
    "AsyncStream",
    "Stream"
]
