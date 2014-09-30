# Module:   interpreter
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Interpreter"""


from rpython.rlib import jit


from . import bytecode
from .errors import Error
from .utils import unquote_string
from .objspace import ObjectSpace
from .objects import Message, Number, String


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

    def peek(self):
        return self.stack[(self.stackp - 1)]

    def empty(self):
        return self.stackp == 0

    @jit.unroll_safe
    def pop_args(self, n):
        args = []
        for _ in xrange(n):
            args.insert(0, self.pop())
        return args


class Interpreter(object):

    _immutable_fields_ = ["bytecode"]

    def __init__(self):
        self.space = ObjectSpace()

    def run(self, bc):  # noqa
        # TODO: Refactor

        pc = 0
        rs = Frame()
        frame = Frame()

        code = bc.code
        receiver = self.space.root

        while pc < len(code):
            try:
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
                    if not rs.empty():
                        receiver = rs.pop()

                    args = frame.pop_args(arg)
                    message = frame.pop()
                    message.args = args
                    result = message.eval(self.space, receiver)
                    frame.push(result)
                    rs.push(result)
                elif c == bytecode.POPRS:
                    rs.pop()
                else:
                    assert AssertionError("Unknown Bytecode: %d" % c)
            except Error as e:
                print e.repr()
                return

        return receiver if rs.empty() else rs.pop()


def interpret(bc):
    return Interpreter().run(bc)
