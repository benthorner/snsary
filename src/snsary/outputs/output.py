from snsary.utils import StrBase


class Output(StrBase):
    def publish(self, reading):
        raise NotImplementedError()
