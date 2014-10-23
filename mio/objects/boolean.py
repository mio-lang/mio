from ..registry import Registry

from .object import W_Object


class W_Boolean(W_Object):

    registry = Registry()

    def __init__(self, space, value, parent=None):
        W_Object.__init__(self, space, parent=(parent or space.object))

        self.value = bool(value)

    def repr(self):
        return "True" if self.value else "False"

    def bool(self):
        return bool(self.value)

    def cmp(self, other):
        assert isinstance(other, W_Boolean)

        if self.value == other.value:
            return 0
        return -1 if self.value < other.value else 1

    def clone(self):
        return self

    def clone_and_init(self, value=None):
        return self
