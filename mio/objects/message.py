from .object import Object


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
            return attr.apply(space, receiver, context, self)

        attr = space.builtins.lookup(self.getname())
        if attr is not None:
            return attr.apply(space, receiver, context, self)

        forward = receiver.lookup("forward")
        if forward is not None:
            return forward.apply(space, receiver, context, self)

        raise AttributeError(
            "%s has no attribute %s" % (receiver, self.getname())
        )
