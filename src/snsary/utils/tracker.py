"""
Utility to track the values of readings with specified names using persistent :mod:`storage <snsary.utils.storage>`. New values are individually compared with old using a specified function e.g. ::

    Tracker('id-for-persistent-storage', myreading=max, othername=min)

Call ``update`` when new readings are available. ``on_change`` is called when one or more tracked values change - set to a different function to subscribe to changes.
"""

from .logger import HasLogger
from .storage import HasStore


class Tracker(HasLogger, HasStore):
    def __init__(self, id, **trackers):
        self.__trackers = trackers
        self.__id = id

    @property
    def values(self):
        return self.store.get(f"{self.__id}-tracked-values", {})

    def on_change(self, old, new):
        pass

    def update(self, readings):
        values = self.values
        new_values = {}

        for name, fn in self.__trackers.items():
            current_value = self.__filter_value(readings, name)

            if not current_value:
                self.logger.debug(f"Tracker missing value for {name}.")
                return

            if name not in values:
                self.logger.debug(f"Tracker filling value for {name}.")
                new_values[name] = current_value
            else:
                new_values[name] = fn(current_value, values[name])

        if new_values == values:
            self.logger.debug("Tracked values unchanged, continuing.")
            return

        self.logger.debug(f"Storing tracked values: {new_values}")
        self.store[f"{self.__id}-tracked-values"] = new_values
        self.on_change(values, new_values)

    def __filter_value(self, readings, name):
        for reading in readings:
            if reading.name == name:
                return reading.value


class MaxTracker(Tracker):
    def __init__(self, id, *, names, on_change):
        self.on_change = on_change
        Tracker.__init__(self, id, **{name: max for name in names})


class NullTracker(Tracker):
    def __init__(self):
        pass

    def update(self, readings):
        """
        Does nothing.
        """
        return

    @property
    def values(self):
        """
        Returns {}.
        """
        return {}
