"""
Base class for anything that needs to perform an action during the ``start`` or ``stop`` phases of a program. This could be something like spawning a thread, or storing data to disk. Each instance of a service is recorded in ``Service.instances`` for use by the :mod:`system <snsary.system>` module.
"""

from .logger import HasLogger
from .storage import HasStore


class Service(HasLogger, HasStore):
    instances = []

    def __init__(self):
        Service.instances += [self]

    @classmethod
    def clear(cls):
        """
        Clear the global list of service instances. For testing use only.
        """
        cls.instances = []

    def start(self):
        """
        Called synchronously by the :mod:`system <snsary.system>` module as part of program startup.
        """
        pass

    def stop(self):
        """
        Called asynchronously by the :mod:`system <snsary.system>` module when a program is stopping. The execution will eventually time out to ensure the overall program stops in good time.
        """
        pass
