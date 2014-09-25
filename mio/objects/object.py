from ..registry import Registry


class Object(object):

    registry = Registry()

    def __init__(self, space, parent=None):
        self.space = space
        self.parent = parent

        self.attrs = {}
        self.registry.populate(self, space)

    def __eq__(self, other):
        return (
            self.__class__ is other.__class__ and
            self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        """NOT_RPYTHON"""

        return self.repr()

    def repr(self):
        return "<%s attrs=%s>" % (self.__class__.__name__, self.attrs.keys())

    def str(self):
        return self.repr()

    def hash(self):
        return sum(map(hash, self.attrs + [self.parent]))

    def lookup(self, name):
        try:
            return self.attrs[name]
        except KeyError:
            if self.parent is not None:
                return self.parent.lookup(name)

    def call(self, space, receiver, context, message):
        return self

    def clone(self):
        return Object(self.space, parent=self)

    def eval(self, space, receiver, context=None):
        return self
