from queue import Queue
from threading import Thread

from snsary.models import EOF

from .logger import logger


class Feed():
    def __init__(self, *, sensors, outputs):
        self.__queues = {}
        self.__output_threads = {}
        self.__sensor_threads = {}

        for sensor in sensors:
            self.__sensor_threads[sensor] = Thread(
                target=self.__broadcast(sensor),
                daemon=True,
                name=str(sensor) + '-relay'
            )

        for output in outputs:
            self.__queues[output] = Queue()

            self.__output_threads[output] = Thread(
                target=self.__relay(output),
                daemon=True,
                name=str(output)
            )

    def start(self):
        for thread in self.__sensor_threads.values():
            logger.debug('Attaching to sensor.')
            thread.start()

        for thread in self.__output_threads.values():
            logger.debug('Starting output.')
            thread.start()

    def stop(self, timeout=1):
        for queue in self.__queues.values():
            queue.put(EOF())

        for sensor, thread in self.__sensor_threads.items():
            thread.join(timeout=timeout)

            if thread.is_alive():
                logger.error(f'Failed to detach {str(sensor)}.')

        for output, thread in self.__output_threads.items():
            thread.join(timeout=timeout)

            if thread.is_alive():
                logger.error(f'Failed to flush {str(output)}.')

    def __broadcast(self, sensor):
        def _loop():
            while True:
                reading = sensor.read()

                if isinstance(reading, EOF):
                    logger.debug('Detached from sensor.')
                    return

                for queue in self.__queues.values():
                    queue.put(reading)

        return _loop

    def __relay(self, output):
        def _loop():
            while True:
                reading = self.__queues[output].get()

                if isinstance(reading, EOF):
                    logger.debug('Flushing output.')
                    output.flush()
                    return

                try:
                    output.send(reading)
                except Exception as e:
                    logger.exception(e)

        return _loop
