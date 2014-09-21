from .object import Object


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
        return self.body.eval(space, receiver, context)
