from ..registry import Registry

from .object import Object


class Number(Object):

    registry = Registry()

    def __init__(self, space, value, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.value = value

    def repr(self):
        return str(self.value)

    def hash(self):
        return hash(self.value)

    def clone(self, value=None):
        return Number(self.space, value or self.value, parent=self)

    @registry.register("+")
    def add(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, Number)

        return receiver.clone(receiver.value + other.value)
