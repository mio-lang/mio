from rply.token import BaseBox


class Message(BaseBox):

    def __init__(self, value):
        self.value = value

    def getvalue(self):
        return self.value

    def __repr__(self):
        """NOT_RPYTHON"""

        return "<Message ({0:s})".format(repr(self.getvalue()))
