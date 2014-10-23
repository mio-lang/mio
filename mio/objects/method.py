from ..registry import Registry

from .object import W_Object


class W_Method(W_Object):

    registry = Registry()

    def __init__(self, space, body=None, args=None, binding=None, parent=None):
        W_Object.__init__(self, space, parent=(parent or space.object))

        self.body = body
        self.args = args if args is not None else []

        self.binding = binding

    def repr(self):
        return "method(...)"

    def str(self):
        return self.repr()

    def hash(self):
        return hash(self.args) + hash(self.body)

    def clone(self):
        return W_Method(self.space, self.body, args=self.args, parent=self)

    def clone_and_init(self, body=None, args=None, binding=None):
        return W_Method(self.space, body, args, parent=self)

    @registry.register("call")
    def m_call(self, space, receiver, context, message):
        """Call Method"""

        # Empty Method
        if self.body is None:
            return

        locals = self.space.locals.clone_and_init(
            receiver, context, message, self,
            parent=(self.binding if self.binding is not None else context)
        )

        return self.body.eval(space, locals)

    @registry.register("bind")
    def m_bind(self, space, receiver, context, message):
        """Bind a Method to an Object"""

        assert len(message.args) == 1

        self.binding = message.args[0].eval(space, context)

        return self
