# Module:   interpreter
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Interpreter"""


from rpython.rlib import jit


from mio import bytecode
from mio.model import Message
from mio.objspace import ObjectSpace


def get_printable_location(pc, code, bc):
    return "%s #%d %s" % (bc.repr(), pc, bytecode.dis_one(code[pc]))


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
        self.stack = [None] * 1024
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


class Interpreter(object):

    def __init__(self):
        self.space = ObjectSpace()

    def eval(self, bc):
        context = self.space.root
        frame = Frame(bc)
        code = bc.code
        pc = 0
        while True:
            jitdriver.jit_merge_point(pc=pc, code=code, bc=bc, frame=frame)

            c = ord(code[pc])
            arg = ord(code[pc + 1])
            pc += 2

            if c == bytecode.LOAD:
                constant = bc.constants[arg]
                frame.push(Message(self.space, constant, value=constant))
            elif c == bytecode.END:
                raise SystemExit(0)
            elif c == bytecode.EVAL:
                name = frame.pop().name
                args = []
                while frame.stack_pos:
                    args.append(frame.pop())
                message = Message(self.space, name, args)
                frame.push(message.eval(self.space, context, context))
            else:
                assert False


def interpret(bc):
    interpreter = Interpreter()
    return interpreter.eval(bc)
