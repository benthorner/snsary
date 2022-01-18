from .logger import HasLogger


class Service(HasLogger):
    instances = []

    def __init__(self):
        Service.instances += [self]

    @classmethod
    def clear(cls):
        cls.instances = []

    def start(self):
        pass

    def stop(self):
        pass
