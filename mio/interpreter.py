# Module:   interpreter
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Interpreter"""


from rpython.rlib import jit
from rpython.rlib.streamio import open_file_as_stream


import mio
from . import bytecode
from .lexer import lex
from .parser import parse
from .errors import Error
from .compiler import compile
from .rreadline import readline
from .utils import unquote_string
from .objspace import ObjectSpace
from .objects import Message, Number, String

BANNER = "%s %s\n" % (mio.__name__, mio.__version__)
PS1 = ">>> "
PS2 = "... "


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

    def __init__(self, debug=False, banner=BANNER, ps1=PS1, ps2=PS2):
        self.debug = debug
        self.banner = banner
        self.ps1 = ps1
        self.ps2 = ps2

        self.space = ObjectSpace()

    def runsource(self, source, filename="<stdin>"):
        ast = parse(lex(source), filename)
        if self.debug:
            print ast.repr()

        bc = compile(ast)
        if self.debug:
            print bc.repr()

        return self.run(bc)

    def runfile(self, filename):
        f = open_file_as_stream(filename)
        source = f.readall()
        f.close()

        return self.runsource(source, filename=filename)

    def repl(self, banner=None, ps1=None, ps2=None):
        banner = banner or self.banner
        ps1 = ps1 or self.ps1
        ps2 = ps2 or self.ps2

        print banner

        while True:
            try:
                s = readline(ps1)
            except EOFError:
                break

            s = s.strip("\n")
            if not s:
                continue

            s = s.encode("utf-8")

            result = self.runsource(s)
            if result is not None:
                print result.repr()

    def run(self, bc):  # noqa
        # TODO: Refactor

        pc = 0
        running = True

        rs = Frame()
        frame = Frame()

        code = bc.code
        receiver = self.space.root

        while pc < len(code) or running:
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
                elif c == bytecode.BIND:
                    args = frame.pop_args(arg)
                    for i in xrange(len(args)):
                        if i < (len(args) - 1):
                            args[i].next = args[(i + 1)]
                    frame.push(args[0])
                elif c == bytecode.EVAL:
                    if not rs.empty():
                        receiver = rs.pop()

                    args = frame.pop_args(arg)
                    message = frame.pop()
                    message.args = args
                    result = message.eval(self.space, receiver)
                    frame.push(result)
                    rs.push(result)
                elif c == bytecode.DROP:
                    rs.pop()
                elif c == bytecode.STOP:
                    break
                else:
                    assert AssertionError("Unknown Bytecode: %d" % c)
            except Error as e:
                print e.repr()
                return

        return receiver if rs.empty() else rs.pop()


def interpret(bc):
    return Interpreter().run(bc)
