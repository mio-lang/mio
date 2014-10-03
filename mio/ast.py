# Module:   ast
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""AST"""


from rply.token import BaseBox


from mio import bytecode


class Node(BaseBox):
    """Base Node"""


class Message(Node):

    def __init__(self, name, args=[], value=None):
        self.name = name
        self.args = args
        self.value = value

        if self.args and self.value is not None:
            raise AssertionError("A literal value cannot contain arguments!")

        self.next = None

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.args == other.args and
            self.value == other.value
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.repr()

    def repr(self):
        s = []

        next = self
        while next is not None:
            if next.getargs():
                args = "(%s)" % ", ".join(
                    [arg.repr() for arg in next.getargs()]
                )
            else:
                args = ""
            s.append("%s%s" % (next.getname(), args))
            next = next.getnext()

        return " ".join(s)

    def getargs(self):
        return self.args

    def setargs(self, args):
        self.args = args

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name

    def getnext(self):
        return self.next

    def setnext(self, next):
        assert isinstance(next, Message)
        self.next = next

    def getvalue(self):
        return self.value

    def setvalue(self, value):
        self.value = value

    def compile(self, ctx, eval=True):
        n = 0
        next = self
        while next is not None:
            n += 1
            args = next.getargs()
            name = next.getname()
            value = next.getvalue()

            if value is not None:
                ctx.emit(bytecode.LOAD, ctx.register_constant(value))
            else:
                ctx.emit(bytecode.LOAD, ctx.register_constant(name))

                for arg in args:
                    n = arg.compile(ctx, False)
                    ctx.emit(bytecode.BIND, n)

            if eval or args:
                ctx.emit(bytecode.EVAL, len(args))
                if not eval:
                    ctx.emit(bytecode.DROP)

            next = next.getnext()
        return n
