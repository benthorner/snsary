from snsary.utils import HasLogger


class Function(HasLogger):
    def __call__(reading):
        raise NotImplementedError()
