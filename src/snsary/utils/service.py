from .strbase import StrBase


class Service(StrBase):
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
