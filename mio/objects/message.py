from pypy.objspace.std.bytesobject import string_escape_encode


from ..errors import Error, LookupError

from .object import Object


class Message(Object):

    def __init__(self, space, name, args=[], value=None, parent=None):
        parent = space.object if parent is None else parent
        Object.__init__(self, space, parent=parent)

        self.name = name
        self.args = args
        self.value = value

        self.next = None

        self.terminator = self.name not in (None, "") and self.name in "\r\n;"

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
        next = self

        while next is not None:
            try:
                if next.terminator:
                    value = context
                elif next.value is not None:
                    value = next.value
                else:
                    name = next.name
                    attr = receiver.lookup(name)
                    if attr is not None:
                        value = attr.call(
                            space, receiver, context, next
                        )
                    else:
                        attr = space.builtins.lookup(name)
                        if attr is not None:
                            value = attr.call(
                                space, receiver, context, next
                            )
                        else:
                            forward = receiver.lookup("forward")
                            if forward is not None:
                                value = forward.call(
                                    space, receiver, context, next
                                )
                            else:
                                raise LookupError(
                                    "%s has no attribute %s" % (
                                        receiver.repr(),
                                        string_escape_encode(name, "'")
                                    )
                                )
                receiver = value
                next = next.next
                # Help out the RPython Annotator
                assert isinstance(next, Message) or next is None
            except Error as e:
                e.stack.append(e)
                raise

        return receiver
