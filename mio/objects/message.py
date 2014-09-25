from pypy.objspace.std.bytesobject import string_escape_encode


from ..errors import LookupError

from .object import Object


class Message(Object):

    def __init__(self, space, name, args=[], value=None, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.name = name
        self.args = args
        self.value = value

        self.terminator = self.name is not None and self.name in "\r\n;"

    def repr(self):
        return "Message(%s, args=%s, value=%s)" % (
            self.name, self.args, self.value
        )

    def hash(self):
        h = hash(self.name)
        for arg in self.args:
            h += arg.hash()
        return h

    def clone(self):
        return Message(
            self.space, self.name, self.args,
            value=self.value, parent=self
        )

    def eval(self, space, receiver, context=None):
        context = receiver if context is None else context

        if self.terminator:
            return context

        name, value = self.name, self.value

        if value is not None:
            return self.value

        attr = receiver.lookup(name)
        if attr is not None:
            return attr.call(space, receiver, context, self)

        attr = space.builtins.lookup(name)
        if attr is not None:
            return attr.call(space, receiver, context, self)

        forward = receiver.lookup("forward")
        if forward is not None:
            return forward.call(space, receiver, context, self)

        raise LookupError(
            "%s has no attribute %s" % (
                receiver.repr(), string_escape_encode(name, "'")
            )
        )
