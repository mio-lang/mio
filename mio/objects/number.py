from .object import Object


class Number(Object):

    def __init__(self, space, number):
        Object.__init__(self, space, [space.object])
        self.value = number

    def repr(self):
        return self.str()

    def str(self):
        return str(self.value)

    def hash(self):
        return hash(self.value)

    def clone(self):
        return Number(self.space, self.value)

    def init(self, value):
        self.value = value
        return self
