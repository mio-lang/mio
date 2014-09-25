#!/usr/bin/env python


"""Main"""


import sys


from rpython.jit.codewriter.policy import JitPolicy
from rpython.rlib.objectmodel import we_are_translated
from rpython.rlib.streamio import fdopen_as_stream, open_file_as_stream

from pypy.objspace.std.bytesobject import string_escape_encode


if not we_are_translated():
    # We can have better repl when running on top of CPython
    import readline  # noqa


import mio
from mio.lexer import lex
from mio.parser import parse
from mio.rpath import basename
from mio.compiler import compile
from mio.interpreter import interpret, Interpreter


def repl():
    stdin = fdopen_as_stream(0, "r")
    stdout = fdopen_as_stream(1, "a")

    interpreter = Interpreter()

    while True:
        if we_are_translated():
            # RPython -- cannot use readline
            stdout.write("> ")
            stdout.flush()
            s = stdin.readline()
        else:
            # CPython -- use readline
            try:
                s = raw_input("> ")
            except (EOFError, KeyboardInterrupt):
                s = ""

        if not s:
            break  # Handle EOF

        s = s.strip("\n")
        if not s:
            continue  # Handle plain ENTER

        tokens = lex(s)
        if not tokens:
            continue  # handle whitespace in RPy

        ast = parse(tokens)

        bc = compile(ast)

        result = interpreter.run(bc)
        if result is not None:
            print result.repr()
    return 0


def run(filename):
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
    print ast.repr()

    print "ByteCode:"
    bc = compile(ast)
    print bc.repr()

    print "Result:"
    print interpret(bc).repr()

    return 0


def usage(prog):
    print "Usage: %s [option] ... [file] [arg] ..." % prog
    print "Options and arguments (and corresponding environment variables):"
    print "  -h to display this help"
    print "  -v to display the version"
    return 0


def version():
    print "mio v%s" % mio.version
    return 0


def main(argv):
    prog = basename(argv[0])

    if len(argv) == 1:
        return repl()
    elif len(argv) == 2:
        if argv[1] == "-h":
            return usage(prog)
        elif argv[1] == "-v":
            return version()
        else:
            return run(argv[1])

    return usage(prog)


def target(driver, args):
    driver.exe_name = "bin/mio"
    return main, None


def jitpolicy(driver):
    return JitPolicy()


if __name__ == "__main__":
    main(sys.argv)
