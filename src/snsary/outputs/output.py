
class Output:
    def flush(self):
        pass

    def filter(self, filter):
        from .filter_output import FilterOutput
        return FilterOutput(self, filter)

    def __str__(self):
        return f'{type(self).__name__.lower()}-{id(self)}'
