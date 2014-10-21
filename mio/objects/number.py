from rpython.rlib.rdtoa import dtoa


from ..registry import Registry

from .object import Object


class Number(Object):

    registry = Registry()

    def __init__(self, space, value=0, parent=None):
        self.value = value

        Object.__init__(self, space, parent=(parent or space.object))

    def repr(self):
        return dtoa(self.value)

    def hash(self):
        return hash(self.value)

    def clone(self):
        return Number(self.space, value=self.value, parent=self)

    def clone_and_init(self, value=0):
        return Number(self.space, value=value, parent=self)

    @registry.register("+")
    def add(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, Number)

        return receiver.clone_and_init(receiver.value + other.value)

    @registry.register("-")
    def sub(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, Number)

        return receiver.clone_and_init(receiver.value - other.value)

    @registry.register("*")
    def mul(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, Number)

        return receiver.clone_and_init(receiver.value * other.value)

    @registry.register("/")
    def div(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, Number)

        return receiver.clone_and_init(receiver.value / other.value)
