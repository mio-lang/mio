# Module:   interpreter
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Interpreter"""


from rpython.rlib import jit


from mio import bytecode
from mio.utils import unquote_string
from mio.objspace import ObjectSpace
from mio.objects import Message, Number, String


def get_printable_location(pc, code, bc):
    return "%s #%d %s" % (bc.repr(), pc, bytecode.dis_one(code[pc]))


jitdriver = jit.JitDriver(
    greens=["pc", "code", "bc"],
    reds=["frame", "self"],
    virtualizables=["frame"],
    get_printable_location=get_printable_location
)


class Frame(object):

    _virtualizable2_ = [
        "stack[*]", "stackp", "parent"
    ]

    def __init__(self, parent=None):
        self = jit.hint(self, fresh_virtualizable=True, access_directly=True)
        self.stack = [None] * 1024
        self.stackp = 0
        self.parent = parent

    def push(self, value):
        pos = self.stackp
        assert pos >= 0
        self.stack[pos] = value
        self.stackp = pos + 1

    def pop(self):
        new_pos = self.stackp - 1
        assert new_pos >= 0
        value = self.stack[new_pos]
        self.stackp = new_pos
        return value


class Interpreter(object):

    _immutable_fields_ = ["bytecode"]

    def __init__(self, bc):
        self.bc = bc

        self.running = False
        self.space = ObjectSpace()

    def run(self):
        self.running = True

        pc = 0
        frame = Frame()

        bc = self.bc
        code = bc.code
        context = self.space.root
        receiver = self.space.root

        while self.running and pc < len(code):
            jitdriver.jit_merge_point(
                bc=bc, code=code, frame=frame, pc=pc, self=self
            )

            c = ord(code[pc])
            arg = ord(code[pc + 1])
            pc += 2

            if c == bytecode.LOAD:
                constant = bc.constants[arg]
                if constant[0] in "'\"":
                    value = String(self.space, unquote_string(constant))
                else:
                    value = Number(self.space, float(constant))
                frame.push(Message(self.space, constant, value=value))
            elif c == bytecode.EVAL:
                constant = bc.constants[arg]
                args = []
                while frame.stackp:
                    args.insert(0, frame.pop())
                message = Message(self.space, constant, args)
                frame.push(message.eval(self.space, context, receiver))
            elif c == bytecode.POP:
                frame.pop()
            elif c == bytecode.END:
                self.running = False
            else:
                assert AssertionError("Unknown Bytecode: %d" % c)
        return receiver


def interpret(bc):
    return Interpreter(bc).run()
