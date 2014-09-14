# Module:   ast
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""AST"""


from rply.token import BaseBox


from mio import bytecode


class Message(BaseBox):

    def __init__(self, name, args=[], value=None):
        self.name = name
        self.args = args
        self.value = value

        self.next = None

    def __repr__(self):
        """NOT_RPYTHON"""

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
        self.next = next

    def compile(self, ctx):
        ctx.emit(bytecode.LOAD, ctx.register_constant(self.value))
