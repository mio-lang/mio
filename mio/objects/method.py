from ..registry import Registry

from .object import Object


class Call(Object):

    def __init__(self, space, receiver, context, message, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.attrs["receiver"] = receiver
        self.attrs["context"] = context
        self.attrs["message"] = message


class Locals(Object):

    def __init__(self, space, receiver, context, message, method, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.receiver = receiver
        self.context = context
        self.message = message
        self.method = method

        self.update_args()
        self.update_call()

    def update_args(self):
        for i in xrange(len(self.method.args)):
            if i < len(self.message.args):
                name = self.method.args[i].name
                value = self.message.args[i].eval(self.space, self.context)
                self.attrs[name] = value

    def update_call(self):
        self.attrs["call"] = Call(
            self.space, self.receiver, self.context, self.message
        )


class Method(Object):

    registry = Registry()

    def __init__(self, space, body, args=None, binding=None, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

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
        return Method(self.space, self.body, args=self.args, parent=self)

    def call(self, space, receiver, context, message):
        # Empty Method
        if self.body is None:
            return

        locals = Locals(
            space, receiver, context, message, self,
            parent=(self.binding if self.binding is not None else context)
        )

        return self.body.eval(space, locals)

    @registry.register()
    def bind(self, space, receiver, context, message):
        """Bind a Method to an Object"""

        assert len(message.args) == 1

        self.binding = message.args[0].eval(space, context)

        return self
