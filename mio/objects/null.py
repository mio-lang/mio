from ..registry import Registry

from .object import W_Object


class W_Null(W_Object):

    registry = Registry()

    def __init__(self, space, parent=None):
        W_Object.__init__(self, space, parent=(parent or space.object))

        self.value = None

    def bool(self):
        return False

    def repr(self):
        return "Null"
