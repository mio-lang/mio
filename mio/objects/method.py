from .object import Object


class Call(Object):

    def __init__(self, space, receiver, context, message, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.attrs["receiver"] = receiver
        self.attrs["context"] = context
        self.attrs["message"] = message


class Locals(Object):

    def __init__(self, space, method, receiver, context, message, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.method = method
        self.receiver = receiver
        self.context = context
        self.message = message

        self.update_args()

    def update_args(self):
        for i in xrange(len(self.method.args)):
            name = self.method.args[i].name
            value = self.message.args[i].eval(self.space, self.context)
            self.attrs[name] = value


class Method(Object):

    def __init__(self, space, body, args=None, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.body = body
        self.args = args if args is not None else []

    def repr(self):
        return "method(...)"

    def str(self):
        return self.repr()

    def hash(self):
        return hash(self.args) + hash(self.body)

    def clone(self):
        return Method(self.space, self.body, args=self.args, parent=self)

    def call(self, space, receiver, context, message):
        locals = Locals(space, self, receiver, context, message)

        return self.body.eval(space, locals)
