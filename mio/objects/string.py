from pypy.objspace.std.bytesobject import string_escape_encode


from .object import Object


class String(Object):

    def __init__(self, space, value, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.value = value

    def repr(self):
        return string_escape_encode(self.value, "'")

    def str(self):
        return self.value

    def hash(self):
        return hash(self.value)

    def clone(self):
        return String(self.space, self.value, parent=self)
