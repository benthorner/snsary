from queue import Queue
from threading import Thread

from snsary.utils import logger

from .stream import Stream


class AsyncStream(Stream):
    def __init__(self):
        self.__relays = {}

    def publish(self, reading):
        for queue in self.__relays.values():
            queue.put(reading)

    def subscribe(self, output):
        queue = Queue()
        self.__relays[output] = queue

        def _relay():
            while True:
                try:
                    output.publish(queue.get())
                except Exception as e:
                    logger.exception(e)

        Thread(
            target=_relay,
            daemon=True,
            name=str(output),
        ).start()
