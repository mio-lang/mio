# Module:   compiler
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Compiler"""


from mio import bytecode
from mio.bytecode import ByteCode


class CompilerContext(object):

    def __init__(self):
        self.data = []
        self.constants = []

    def register_constant(self, value):
        self.constants.append(value)
        return len(self.constants) - 1

    def emit(self, bc, arg=0):
        self.data.append(chr(bc))
        self.data.append(chr(arg))

    def create_bytecode(self):
        return ByteCode("".join(self.data), self.constants[:])


def compile(node):
    ctx = CompilerContext()
    node.compile(ctx)
    ctx.emit(bytecode.END)
    return ctx.create_bytecode()
