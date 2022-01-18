from datetime import datetime
from threading import Event, Thread

from .logger import get_logger
from .service import Service


class Poller(Service):
    def __init__(self, *, period_seconds):
        Service.__init__(self)
        self.__period = period_seconds
        self.__stop = Event()
        self.__thread = Thread(target=self.__loop, daemon=True)

    @property
    def period(self):
        return self.__period

    def start(self):
        self.__start_time = datetime.utcnow()
        self.__thread.start()

    def stop(self):
        self.__stop.set()
        self.__thread.join()

    def __loop(self):
        while not self.__stop.is_set():
            now = datetime.utcnow()
            self._tick(**self.__tick_kwargs(now))
            delay = int((datetime.utcnow() - now).total_seconds())

            if delay > self.period:
                get_logger().warning(f"Took too long to get sample: {delay}s.")
            else:
                self.__stop.wait(timeout=(self.period - delay))

    def _tick(self, **kwargs):
        pass

    def __tick_kwargs(self, now):
        return {
            "now": now,
            "start_time": self.__start_time,
            "timestamp_seconds": int(now.timestamp()),
            "elapsed_seconds": int((now - self.__start_time).total_seconds())
        }
