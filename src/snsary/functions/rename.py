"""
Maps each :mod:`Reading <snsary.models.reading>` to a new one with the name altered as specified. This can be useful to distinguish the same :mod:`Readings <snsary.models.reading>` being aggregated in different ways.
"""

from snsary.models import Reading

from .function import Function


class Rename(Function):
    def __init__(self, append=''):
        self.__append = append

    def __call__(self, reading):
        return [Reading(
            sensor=reading.sensor,
            name=f'{reading.name}{self.__append}',
            timestamp_seconds=reading.timestamp,
            value=reading.value
        )]
