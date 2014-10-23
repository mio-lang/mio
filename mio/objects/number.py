from rpython.rlib.rdtoa import dtoa


from ..registry import Registry

from .object import W_Object


class W_Number(W_Object):

    registry = Registry()

    def __init__(self, space, value=0, parent=None):
        W_Object.__init__(self, space, parent=(parent or space.object))

        self.value = value

    def repr(self):
        return dtoa(self.value)

    def hash(self):
        return hash(self.value)

    def clone(self):
        return W_Number(self.space, value=self.value, parent=self)

    def clone_and_init(self, value=0):
        return W_Number(self.space, value=value, parent=self)

    @registry.register("+")
    def m_add(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, W_Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, W_Number)

        return receiver.clone_and_init(receiver.value + other.value)

    @registry.register("-")
    def m_sub(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, W_Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, W_Number)

        return receiver.clone_and_init(receiver.value - other.value)

    @registry.register("*")
    def m_mul(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, W_Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, W_Number)

        return receiver.clone_and_init(receiver.value * other.value)

    @registry.register("/")
    def m_div(self, space, receiver, context, message):
        assert len(message.args) == 1
        assert isinstance(receiver, W_Number)

        other = message.args[0].eval(space, context)
        assert isinstance(other, W_Number)

        return receiver.clone_and_init(receiver.value / other.value)
