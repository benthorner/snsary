from threading import Event

from snsary.utils import logger

from .output import Output


class MockOutput(Output):
    def __init__(
        self,
        *,
        fail=False,
        hang=False,
    ):
        self.__hang = hang
        self.__fail = fail
        self.__failures = 0

    def flush(self):
        if self.__hang:
            Event().wait()

    def send(self, reading):
        if self.__fail:
            self.__failures += 1
            raise RuntimeError(f'problem-{self.__failures}')

        logger.info(f"Reading: {reading}")
