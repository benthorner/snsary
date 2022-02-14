"""
Computes a mean average of :mod:`Readings <snsary.models.reading>` over fixed, consecutive windows.
"""

from statistics import mean

from snsary.models import Reading

from .window import Window


class WindowAverage(Window):
    def aggregate(self, readings):
        return [Reading(
            sensor_name=readings[0].sensor_name,
            name=readings[0].name,
            timestamp=readings[-1].timestamp,
            value=mean(r.value for r in readings)
        )]
