from datetime import datetime

from snsary.utils import Service, logger

from .output import Output


class BatchOutput(Output, Service):
    def __init__(self, *, max_size=100, max_wait_seconds=10):
        Output.__init__(self)
        self.__max_size = max_size
        self.__readings = []
        self.__max_wait_seconds = max_wait_seconds
        self.__last_publish = datetime.utcnow().timestamp()

    def flush(self):
        logger.info(f"Sending {len(self.__readings)} readings.")
        self.publish_batch(self.__readings)
        self.__readings = []

    def stop(self):
        if self.__readings:
            self.flush()

    def publish(self, reading):
        self.__readings += [reading]
        self.__try_publish_large_batch()
        self.__try_publish_old_batch()

    def __try_publish_large_batch(self):
        if len(self.__readings) < self.__max_size:
            return

        self.flush()

    def __try_publish_old_batch(self):
        now = datetime.utcnow().timestamp()
        delay = now - self.__last_publish

        if delay > self.__max_wait_seconds:
            self.flush()
            self.__last_publish = now