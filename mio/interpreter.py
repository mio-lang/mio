# Module:   interpreter
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Interpreter"""


from rpython.rlib import jit


from mio import bytecode
from mio.ast import Message


def get_printable_location(pc, code, bc):
    return "%s #%d %s" % (bc.get_repr(), pc, bytecode.dis_one(code[pc]))


jitdriver = jit.JitDriver(
    greens=["pc", "code", "bc"],
    reds=["frame"],
    virtualizables=["frame"],
    get_printable_location=get_printable_location
)


class Frame(object):

    _virtualizable2_ = [
        "stack[*]", "stack_pos", "parent"
    ]

    def __init__(self, bc, parent=None):
        self = jit.hint(self, fresh_virtualizable=True, access_directly=True)
        self.stack = [None] * 10
        self.stack_pos = 0
        self.parent = parent

    def push(self, value):
        pos = self.stack_pos
        assert pos >= 0
        self.stack[pos] = value
        self.stack_pos = pos + 1

    def pop(self):
        new_pos = self.stack_pos - 1
        assert new_pos >= 0
        value = self.stack[new_pos]
        self.stack_pos = new_pos
        return value


def execute(frame, bc):
    code = bc.code
    pc = 0
    while True:
        jitdriver.jit_merge_point(pc=pc, code=code, bc=bc, frame=frame)

        c = ord(code[pc])
        arg = ord(code[pc + 1])
        pc += 2

        if c == bytecode.LOAD:
            frame.push(Message(bc.constants[arg]))
        elif c == bytecode.END:
            return
        else:
            assert False


def interpret(bc):
    frame = Frame(bc)
    execute(frame, bc)
    return frame
