import signal
from threading import Event, Thread

from snsary.utils import Service, logger


def start():
    for service in Service.instances:
        logger.debug(f"Starting {str(service)}.")
        service.start()

    logger.info("Started.")


def start_and_wait():
    start()
    wait()


def stop(*_):
    logger.info('Stopping.')

    for service in Service.instances:
        __stop_service(service)

    logger.info('Bye.')


def wait(*, handle_signals=True):
    if handle_signals:
        signal.signal(signal.SIGINT, stop)
        signal.signal(signal.SIGTERM, stop)

    class Waiter(Service):
        def __init__(self):
            Service.__init__(self)
            self.__event = Event()

        def wait(self):
            self.__event.wait()

        def stop(self):
            self.__event.set()

    Waiter().wait()


def __stop_service(service):
    logger.debug(f'Stopping {str(service)}.')
    thread = Thread(target=service.stop, daemon=True)
    thread.start()

    thread.join(timeout=1)
    logger.debug(f'Stopped {str(service)}.')

    if thread.is_alive():
        logger.error(f'Failed to stop {str(service)}.')
