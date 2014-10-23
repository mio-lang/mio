from pypy.objspace.std.bytesobject import string_escape_encode


from .object import W_Object


class W_String(W_Object):

    def __init__(self, space, value="", parent=None):
        self.value = value

        W_Object.__init__(self, space, parent=(parent or space.object))

    def repr(self):
        return string_escape_encode(self.value, "'")

    def str(self):
        return self.value

    def hash(self):
        return hash(self.value)

    def clone(self):
        return W_String(self.space, value=self.value, parent=self)

    def clone_and_init(self, value=""):
        return W_String(self.space, value=value, parent=self)
