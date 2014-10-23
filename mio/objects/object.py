from ..registry import Registry


class Object(object):

    registry = Registry()

    def __init__(self, space, parent=None):
        self.space = space
        self.parent = parent

        self.attrs = {}

    def __eq__(self, other):
        return (
            self.__class__ is other.__class__ and
            self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()

    def repr(self):
        return "<%s attrs=%s>" % (self.__class__.__name__, self.attrs.keys())

    def str(self):
        return self.repr()

    def hash(self):
        return sum(map(hash, self.attrs + [self.parent]))

    def type(self):
        return self.__class__.__name__

    def lookup(self, name):
        try:
            return self.attrs[name]
        except KeyError:
            if self.parent is not None:
                return self.parent.lookup(name)

    def call(self, space, receiver, context, message):
        return self

    def clone(self):
        return Object(self.space, self)

    def eval(self, space, receiver, context=None):
        return self

    @registry.register("clone")
    def m_clone(self, space, receiver, context, message):
        """Create a new Object by cloning the receiver"""

        assert isinstance(receiver, Object)

        return receiver.clone()

    @registry.register("type")
    def m_type(self, space, receiver, context, message):
        """Returns Object Type"""

        return self.space.string.clone_and_init(receiver.type())
