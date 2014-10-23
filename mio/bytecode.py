# Module:   bytecode
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Bytecode"""


from pypy.objspace.std.bytesobject import string_escape_encode


bytecodes = [
    "BIND",     # Bind messages on the stack into a message chain (arguments)
    "PUSH",     # Push a new message on the stack from a message and arguments
    "DROP",     # Discard the top of the receiver stack (arguments)
    "LOAD",     # Load a constant value onto the stack
    "EVAL",     # Evaluate the message on the top of the stack with arguments
    "STOP",     # Terminate the interpreter (virtual machone)
]


globals().update(dict((bytecode, i) for i, bytecode in enumerate(bytecodes)))


def dis_one(code):
    return bytecodes[ord(code)]


class ByteCode(object):

    _immutable_fields_ = ["code", "constants[*]"]

    def __init__(self, code, constants):
        self.code = code
        self.constants = constants

    def dump_code(self):
        lines = []
        i = 0
        for i in range(0, len(self.code), 2):
            c = self.code[i]
            c2 = self.code[i + 1]
            lines.append(bytecodes[ord(c)] + " " + str(ord(c2)))
        return "\n".join(lines)

    def dump_constants(self):
        lines = []
        i = 0
        for i in range(0, len(self.constants)):
            lines.append(
                str(i) + ": " + string_escape_encode(self.constants[i], "'")
            )
        return "\n".join(lines)

    def repr(self):
        lines = []

        lines.append("Code:")
        lines.append(self.dump_code())

        lines.append("Constants:")
        lines.append(self.dump_constants())

        return "\n".join(lines)
