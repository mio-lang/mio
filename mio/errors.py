class MioError(Exception):
    """Mio Error"""

    def __init__(self, value):
        self.value = value

        self.stack = []

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()

    def repr(self):
        return "%s: %s" % (self.__class__.__name__, self.value)

    def str(self):
        return self.repr()


class MioLookupError(MioError):
    """Mio Lookup Error"""


class MioTypeError(MioError):
    """Mio Type Error"""


class MioSyntaxError(MioError):
    """Mio Syntax Error"""
