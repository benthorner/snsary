import signal
from threading import Event, Thread

from snsary.utils import Service, get_logger


def start():
    for service in Service.instances:
        service.logger.debug("Starting.")
        service.start()

    get_logger().info("Started.")


def start_and_wait():
    start()
    wait()


def stop(*_):
    get_logger().info('Stopping.')

    for service in Service.instances:
        __stop_service(service)

    get_logger().info('Bye.')


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
    service.logger.debug("Stopping.")
    thread = Thread(target=service.stop, daemon=True)
    thread.start()

    thread.join(timeout=1)
    service.logger.debug("Stopped.")

    if thread.is_alive():
        service.logger.error("Failed to stop.")
