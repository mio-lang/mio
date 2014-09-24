from .object import Object


class CFunction(Object):

    def __init__(self, space, name, func):
        Object.__init__(self, space, [space.object])

        self.name = name
        self.func = func

    def repr(self):
        return "<CFunctions name='%s'>" % self.name

    def hash(self):
        return hash(self.func)

    def clone(self):
        return CFunction(self.space, self.name, self.func)

    def init(self, name, func):
        return self

    def call(self, space, receiver, context, message):
        # TODO: Evaluate message arguments
        # TODO: Convert between mio and C/RPython types
        return self.func(receiver, space, receiver, context, message)
