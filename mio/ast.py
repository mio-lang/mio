# Module:   ast
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""AST"""


from rply.token import BaseBox


from mio import bytecode


class Message(BaseBox):

    def __init__(self, value):
        self.value = value

    def getvalue(self):
        return self.value

    def compile(self, ctx):
        ctx.emit(bytecode.LOAD, ctx.register_constant(self.value))
