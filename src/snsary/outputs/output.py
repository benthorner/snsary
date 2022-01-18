from snsary.utils import HasLogger


class Output(HasLogger):
    def publish(self, reading):
        raise NotImplementedError()
