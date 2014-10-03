#!/usr/bin/env python


"""Main"""


import sys


from rpython.jit.codewriter.policy import JitPolicy
from rpython.rlib.streamio import fdopen_as_stream, open_file_as_stream


import mio
from mio.lexer import lex
from mio.parser import parse
from mio.rpath import basename
from mio.compiler import compile
from mio.interpreter import interpret, Interpreter


class Options(object):
    """Options Container"""


def repl(debug=False):
    stdin = fdopen_as_stream(0, "r")
    stdout = fdopen_as_stream(1, "a")

    interpreter = Interpreter()

    stdout.write("%s %s\n" % (mio.__name__, mio.__version__))

    while True:
        stdout.write("> ")
        stdout.flush()
        s = stdin.readline()

        if not s:
            break  # Handle EOF

        s = s.strip("\n")
        if not s:
            continue  # Handle plain ENTER

        ast = parse(lex(s))
        if debug:
            print ast.repr()

        bc = compile(ast)
        if debug:
            print bc.repr()

        result = interpreter.run(bc)
        if result is not None:
            print result.repr()

    return 0


def run(filename, debug=False):
    f = open_file_as_stream(filename)
    source = f.readall()
    f.close()

    ast = parse(lex(source), filename)
    if debug:
        print ast.repr()

    bc = compile(ast)
    if debug:
        print bc.repr()

    result = interpret(bc)
    if result is not None:
        print result

    return 0


def usage(prog):
    print "Usage: %s [options] [file]" % prog
    return 0


def help():
    print "Options and Arguments:"
    print "  -d debug output"
    print "  -h to display this help"
    print "  -v to display the version"
    return 0


def version():
    print "mio v%s" % mio.version
    return 0


def parse_bool_arg(name, argv, default=False):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del argv[i]
            return True
    return default


def parse_arg(name, argv, default=""):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del argv[i]
            return argv.pop(i)
    return default


def parse_args(argv):
    opts = Options()

    opts.debug = parse_bool_arg('-d', argv)
    opts.help = parse_bool_arg("-h", argv)
    opts.version = parse_bool_arg("-v", argv)

    del argv[0]

    return opts, argv


def main(argv):
    prog = basename(argv[0])
    opts, args = parse_args(argv)

    if opts.help:
        usage(prog)
        return help()

    if opts.version:
        return version()

    if args:
        return run(args[0], debug=opts.debug)

    return repl(debug=opts.debug)


def target(driver, args):
    driver.exe_name = "bin/mio"
    return main, None


def jitpolicy(driver):
    return JitPolicy()


if __name__ == "__main__":
    main(sys.argv)
