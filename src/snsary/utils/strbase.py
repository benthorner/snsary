class StrBase:
    def __str__(self):
        return f'{type(self).__name__.lower()}-{id(self)}'
