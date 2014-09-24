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

    def __init__(self):
        self.space = ObjectSpace()

    def run(self, bc):
        pc = 0
        frame = Frame()

        code = bc.code
        context = self.space.root
        receiver = self.space.root

        while pc < len(code):
            jitdriver.jit_merge_point(
                bc=bc, code=code, frame=frame, pc=pc, self=self
            )

            c = ord(code[pc])
            arg = ord(code[pc + 1])
            pc += 2

            if c == bytecode.LOAD:
                constant = bc.constants[arg]
                c = constant[0]
                if c == "-" or c.isdigit():
                    value = Number(self.space, float(constant))
                elif constant[0] in "'\"":
                    value = String(self.space, unquote_string(constant))
                else:
                    value = None
                frame.push(Message(self.space, constant, value=value))
            elif c == bytecode.EVAL:
                args = pop_args(frame, arg)
                message = frame.pop()
                message.setargs(args)
                frame.push(message.eval(self.space, context, receiver))
            else:
                assert AssertionError("Unknown Bytecode: %d" % c)
        return receiver


@jit.unroll_safe
def pop_args(frame, n):
    args = []
    for _ in xrange(n):
        args.insert(0, frame.pop())
    return args


def interpret(bc):
    return Interpreter().run(bc)
