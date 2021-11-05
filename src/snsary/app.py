import signal
from threading import Event

from snsary.utils import Feed, logger


class App:
    def __init__(self, *, sensors, outputs):
        self.__sensors = sensors
        self.__stop = Event()

        self.__feed = Feed(
            sensors=sensors,
            outputs=outputs
        )

    def start(self):
        self.__feed.start()

        for sensor in self.__sensors:
            sensor.start()

        logger.info("Started.")

    def wait(self):
        self.__stop.wait()
        logger.info("Bye.")

    def stop(self, *_):
        logger.info("Stopping.")

        for sensor in self.__sensors:
            sensor.stop()

        self.__feed.stop()
        self.__stop.set()

    def handle_signals(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
