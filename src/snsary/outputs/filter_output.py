from .output import Output


class FilterOutput(Output):
    def __init__(self, output, filter):
        self.__output = output
        self.__filter = filter

    def send(self, reading):
        if self.__filter(reading):
            self.__output.send(reading)

    def __str__(self):
        return str(self.__output) + ' (filtered)'
