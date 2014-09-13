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
        """NOT RPYTHON"""

        s = []

        next = self
        while next is not None:
            if next.args:
                args = "(%s)" % ", ".join([repr(arg) for arg in next.args])
            else:
                args = ""
            s.append("%s%s" % (next.name, args))
            next = next.next

        return "".join(s)

    def setargs(self, args):
        self.args = args

    def setnext(self, next):
        self.next = next

    def compile(self, ctx):
        ctx.emit(bytecode.LOAD, ctx.register_constant(self.value))
