"""
Maps each :mod:`Reading <snsary.models.reading>` to a new one with the name altered as specified. This can be useful to distinguish the same :mod:`Readings <snsary.models.reading>` being aggregated in different ways.

Supported alterations include:

    - ``to`` - replaces the name of the reading with the one specified.
    - ``append`` - adds to the new or existing name of the reading.
"""

from snsary.models import Reading

from .function import Function


class Rename(Function):
    def __init__(self, append='', to=None):
        self.__append = append
        self.__to = to

    def __call__(self, reading):
        new_name = self.__to if self.__to else reading.name
        new_name += self.__append

        return [Reading(
            sensor_name=reading.sensor_name,
            name=new_name,
            timestamp=reading.timestamp,
            value=reading.value
        )]
