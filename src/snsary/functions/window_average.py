"""
Computes a mean average of :mod:`Readings <snsary.models.reading>` over fixed, consecutive windows.
"""

from statistics import mean

from snsary.models import Reading

from .window import Window


class WindowAverage(Window):
    def _aggregate(self, readings):
        return [Reading(
            sensor=readings[0].sensor,
            name=readings[0].name,
            timestamp_seconds=readings[-1].timestamp,
            value=mean(r.value for r in readings)
        )]
