from .object import Object


class Number(Object):

    def __init__(self, space, value, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.value = value

    def repr(self):
        return str(self.value)

    def hash(self):
        return hash(self.value)

    def clone(self):
        return Number(self.space, self.value, parent=self)
