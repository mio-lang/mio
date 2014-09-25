class Error(Exception):
    """Error"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, self.value)


class LookupError(Error):
    """Lookup Error"""


class TypeError(Error):
    """Type Error"""


class SyntaxError(Error):
    """Syntax Error"""
