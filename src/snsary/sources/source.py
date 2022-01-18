from snsary.utils import HasLogger


class Source(HasLogger):
    def subscribe(self, output):
        raise NotImplementedError()
