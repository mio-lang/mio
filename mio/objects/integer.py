from ..registry import Registry

from .number import Number


class Integer(Number):

    registry = Registry()

    def __init__(self, space, value=0, parent=None):
        Number.__init__(self, space, parent=(parent or space.number))

        self.value = value

    def clone(self):
        return Integer(self.space, value=self.value, parent=self)

    def clone_and_init(self, value=0):
        return Integer(self.space, value=value, parent=self)
