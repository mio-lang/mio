from pypy.objspace.std.bytesobject import string_escape_encode


from .object import Object


class String(Object):

    def __init__(self, space, string):
        Object.__init__(self, space, [space.object])
        self.value = string

    def repr(self):
        return string_escape_encode(self.value, "'")

    def str(self):
        return self.value

    def hash(self):
        return hash(self.value)

    def clone(self):
        return String(self.space, self.value, [self])

    def init(self, value):
        self.value = value
        return self
