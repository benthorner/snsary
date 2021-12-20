from snsary.utils import StrBase


class Source(StrBase):
    def subscribe(self, output):
        raise NotImplementedError()
