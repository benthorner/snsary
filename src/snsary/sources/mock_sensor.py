from threading import Event

from snsary.models import Reading

from .polling_sensor import PollingSensor


class MockSensor(PollingSensor):
    def __init__(
        self,
        *,
        fail=False,
        hang=False,
        period_seconds=5
    ):
        PollingSensor.__init__(
            self,
            name='mocksensor',
            period_seconds=period_seconds
        )

        self.__hang = hang
        self.__fail = fail
        self.__failures = 0

    def sample(
        self,
        now,  # unused here
        start_time,  # unused here
        timestamp_seconds,
        elapsed_seconds
    ):
        if self.__fail:
            self.__failures += 1
            raise RuntimeError(f'problem-{self.__failures}')

        if self.__hang:
            Event().wait()

        return [
            Reading(
                sensor=self,
                name='zero',
                timestamp_seconds=timestamp_seconds,
                value=elapsed_seconds,
            )
        ]