# Module:   model
# Date:     9th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Model"""


class Object(object):

    def __init__(self, space, protos=[]):
        self.space = space
        self.protos = protos

        self.attrs = {}

    def __eq__(self, other):
        return (
            self.__class__ is other.__class__ and
            self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self == other

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

    def apply(self, space, receiver, message, context):
        return self

    def clone(self):
        return Object(self.space, [self])

    def __repr__(self):
        """NOT_RPYTHON"""

        return "<%s attrs=%s>" % (self.__class__.__name__, self.attrs.keys(),)


class String(Object):

    def __init__(self, space, string):
        Object.__init__(self, space, [space.object])
        self.value = string

    def hash(self):
        return hash(self.value)

    def clone(self):
        return String(self.space, self.value, [self])

    def init(self, value):
        self.value = value
        return self

    def __repr__(self):
        """NOT_RPYTHON"""

        return "<String value='%s'>" % self.value


class Message(Object):

    def __init__(self, space, name, args=[], value=None):
        Object.__init__(self, space, [space.object])
        self.name = name
        self.args = args
        self.value = value

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name

    def getargs(self):
        return self.args

    def setargs(self, args):
        self.args = args

    def getvalue(self):
        return self.value

    def setvalue(self, value):
        self.value = value

    def __repr__(self):
        """NOT_RPYTHON"""

        return "Message(%s, args=%r, value=%r)" % (
            self.name, self.args, self.value
        )

    def hash(self):
        h = hash(self.name)
        for arg in self.args:
            h += arg.hash()
        return h

    def eval(self, space, receiver, context):
        if self.getname() == ";":
            return context

        if self.getvalue() is not None:
            return self

        attr = receiver.lookup(self.getname())
        if attr is not None:
            return attr.apply(space, receiver, self, context)

        forward = receiver.lookup("forward")
        if forward is not None:
            return forward.apply(space, receiver, self, context)

        raise AttributeError(
            "%s has no attribute %s" % (receiver, self.getname())
        )
