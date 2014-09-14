from .object import Object


class String(Object):

    def __init__(self, space, string):
        Object.__init__(self, space, [space.object])
        self.value = string

    def hash(self):
        return hash(self.value)

    def clone(self):
        return String(self.space, self.value, [self])

    def init(self, value):
        self.value = value
        return self

    def __repr__(self):
        """NOT_RPYTHON"""

        return "<String value='%s'>" % self.value
