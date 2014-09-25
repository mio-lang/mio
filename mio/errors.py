class Error(Exception):
    """Error"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()

    def repr(self):
        return "%s: %s" % (self.__class__.__name__, self.value)

    def str(self):
        return self.repr()


class LookupError(Error):
    """Lookup Error"""


class TypeError(Error):
    """Type Error"""


class SyntaxError(Error):
    """Syntax Error"""
