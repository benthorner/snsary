from datetime import datetime

from snsary.utils import logger

from .output import Output


class BatchOutput(Output):
    def __init__(self, *, max_size=100, max_wait_seconds=10):
        Output.__init__(self)
        self.__max_size = max_size
        self.__readings = []
        self.__max_wait_seconds = max_wait_seconds
        self.__last_send = datetime.utcnow().timestamp()

    def flush(self):
        logger.info(f"Sending {len(self.__readings)} readings.")
        self.send_batch(self.__readings)
        self.__readings = []

    def send(self, reading):
        self.__readings += [reading]
        self.__try_send_large_batch()
        self.__try_send_old_batch()

    def __try_send_large_batch(self):
        if len(self.__readings) < self.__max_size:
            return

        self.flush()

    def __try_send_old_batch(self):
        now = datetime.utcnow().timestamp()
        delay = now - self.__last_send

        if delay > self.__max_wait_seconds:
            self.flush()
            self.__last_send = now
