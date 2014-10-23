from .object import W_Object


class W_CFunction(W_Object):

    def __init__(self, space, name, func, parent=None):
        W_Object.__init__(self, space, parent=(parent or space.object))

        self.name = name
        self.func = func

    def repr(self):
        return "<CFunctions name='%s'>" % self.name

    def hash(self):
        return hash(self.name) + hash(self.func)

    def call(self, space, receiver, context, message):
        # TODO: Evaluate message arguments
        # TODO: Convert between mio and C/RPython types
        return self.func(receiver, space, receiver, context, message)

    def clone(self):
        return W_CFunction(self.space, self.name, self.func, parent=self)
