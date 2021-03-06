from ..registry import Registry

from .number import W_Number


class W_Integer(W_Number):

    registry = Registry()

    def __init__(self, space, value=0, parent=None):
        W_Number.__init__(self, space, value, parent=(parent or space.number))

    def clone(self):
        return W_Integer(self.space, value=self.value, parent=self)

    def clone_and_init(self, value=0):
        return W_Integer(self.space, value=value, parent=self)
