from threading import Event

from .output import Output


class MockOutput(Output):
    def __init__(
        self,
        *,
        fail=False,
        hang=False,
    ):
        self.__fail = fail
        self.__hang = hang
        self.__failures = 0

    def publish(self, reading):
        if self.__hang:
            Event().wait()

        if self.__fail:
            self.__failures += 1
            raise RuntimeError(f'problem-{self.__failures}')

        self.logger.info(f"Reading: {reading}")
