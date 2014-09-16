from .object import Object


class CFunction(Object):

    def __init__(self, space, name, func):
        Object.__init__(self, space, [space.object])

        self.name = name
        self.func = func

    def hash(self):
        return hash(self.func)

    def clone(self):
        return CFunction(self.space, self.name, self.func)

    def init(self, name, func):
        return self

    def apply(self, space, receiver, context, message):
        # TODO: Evaluate message arguments
        # TODO: Convert between mio and C/RPython types
        return self.func(space, receiver, context, message)

    def __repr__(self):
        """NOT_RPYTHON"""

        return "<CFunctions name='%s'>" % self.name
