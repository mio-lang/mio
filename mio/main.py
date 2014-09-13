#!/usr/bin/env python


"""Usage: mio <filename>"""


import sys


from rpython.jit.codewriter.policy import JitPolicy
from rpython.rlib.streamio import open_file_as_stream
from pypy.objspace.std.bytesobject import string_escape_encode


from mio.lexer import lex
from mio.parser import parse
from mio.compiler import compile
from mio.interpreter import interpret


def main(argv):
    if not len(argv) == 2:
        print __doc__
        return 1

    filename = argv[1]
    f = open_file_as_stream(filename)
    source = f.readall()
    f.close()

    print "Tokens:"
    tokens = lex(source)

    for token in tokens:
        print "<Token (%s, %s)>" % (
            token.name,
            string_escape_encode(token.value, "'")
        )

    print "AST:"
    ast = parse(lex(source), filename)
    print repr(ast)

    print "Compile:"
    bc = compile(ast)
    print string_escape_encode(bc.dump(), "'")

    print "Interpret:"
    frame = interpret(bc)
    for value in frame.stack:
        print value

    return 0


def target(driver, args):
    driver.exe_name = "bin/mio"
    return main, None


def jitpolicy(driver):
    return JitPolicy()


if __name__ == "__main__":
    main(sys.argv)
