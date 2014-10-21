from ..registry import Registry

from .number import Number


class Float(Number):

    registry = Registry()

    def __init__(self, space, value=0, parent=None):
        Number.__init__(self, space, parent=(parent or space.number))

        self.value = value

    def clone(self):
        return Float(self.space, value=self.value, parent=self)

    def clone_and_init(self, value=0):
        return Float(self.space, value=value, parent=self)
