# Module:   bytecode
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Bytecode"""


bytecodes = [
    "LOAD",
    "PUSH",
    "GET",
    "SET",
    "NEW",
    "EVAL",
    "END",
]


globals().update(dict((bytecode, i) for i, bytecode in enumerate(bytecodes)))


def dis_one(code):
    return bytecodes[ord(code)]


class ByteCode(object):

    _immutable_fields_ = ["code", "constants[*]"]

    def __init__(self, code, constants):
        self.code = code
        self.constants = constants

    def dump(self):
        lines = []
        i = 0
        for i in range(0, len(self.code), 2):
            c = self.code[i]
            c2 = self.code[i + 1]
            lines.append(bytecodes[ord(c)] + " " + str(ord(c2)))
        return "\n".join(lines)

    def get_repr(self):
        return "<code object ...>"
