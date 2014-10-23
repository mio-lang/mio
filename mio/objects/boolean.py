from ..registry import Registry

from .object import Object


class Boolean(Object):

    registry = Registry()

    def __init__(self, space, value, parent=None):
        Object.__init__(self, space, parent=(parent or space.object))

        self.value = bool(value)

    def repr(self):
        return "True" if self.value else "False"

    def clone(self):
        return self

    def clone_and_init(self, value=None):
        return self
