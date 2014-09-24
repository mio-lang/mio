from .object import Object


class Call(Object):

    def __init__(self, space, receiver, context, message):
        Object.__init__(self, space, [space.object])

        self.attrs["receiver"] = receiver
        self.attrs["context"] = context
        self.attrs["message"] = message


class Locals(Object):

    def __init__(self, space, method, receiver, context, message):
        Object.__init__(self, space, [space.object])

        self.method = method
        self.receiver = receiver
        self.context = context
        self.message = message

        self.update_args()

    def update_args(self):
        for i in xrange(len(self.method.args)):
            name = self.method.args[i].name

            value = self.message.args[i].eval(
                self.space, self.context, self.context
            )

            self.attrs[name] = value


class Method(Object):

    def __init__(self, space, body, args=None):
        Object.__init__(self, space, [space.object])

        self.body = body
        self.args = args if args is not None else []

    def repr(self):
        return "method(...)"

    def str(self):
        return self.repr()

    def hash(self):
        return hash(self.args) + hash(self.body)

    def clone(self):
        return Method(self.space, self.body, args=self.args)

    def init(self, body, args=None):
        self.body = body
        self.args = args if args is not None else []
        return self

    def call(self, space, receiver, context, message):
        locals = Locals(space, self, receiver, context, message)

        return self.body.eval(space, locals, locals)
