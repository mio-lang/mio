from pypy.objspace.std.bytesobject import string_escape_encode


from .object import Object


class String(Object):

    def __init__(self, space, value="", parent=None):
        self.value = value

        Object.__init__(self, space, parent=(parent or space.object))

    def repr(self):
        return string_escape_encode(self.value, "'")

    def str(self):
        return self.value

    def hash(self):
        return hash(self.value)

    def clone(self):
        return String(self.space, value=self.value, parent=self)

    def clone_and_init(self, value=""):
        return String(self.space, value=value, parent=self)
