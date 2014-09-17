from .object import Object


class Number(Object):

    def __init__(self, space, number):
        Object.__init__(self, space, [space.object])
        self.value = number

    def repr(self):
        return str(self.value)

    def hash(self):
        return hash(self.value)

    def clone(self):
        return Number(self.space, self.value, [self])

    def init(self, value):
        self.value = value
        return self
