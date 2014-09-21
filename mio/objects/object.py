from ..registry import Registry


class Object(object):

    registry = Registry()

    def __init__(self, space, protos=[]):
        self.space = space
        self.protos = protos

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

    def hash(self):
        h = 0
        for attr in self.attrs:
            h += attr.hash()
        for proto in self.protos:
            h += hash(proto)

        return h

    def lookup(self, name, seen=None):
        if seen is None:
            seen = {}
        else:
            if self in seen:
                return None
        seen[self] = None

        try:
            return self.attrs[name]
        except KeyError:
            pass
        for x in self.protos:
            t = x.lookup(name, seen)
            if t is not None:
                return t

    def apply(self, space, receiver, context, message):
        return self

    def clone(self):
        return Object(self.space, [self])
