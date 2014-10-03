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


def runsource(source, filename="<stdin>", debug=False):
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


def runfile(filename, debug=False):
    f = open_file_as_stream(filename)
    source = f.readall()
    f.close()

    return runsource(source, filename=filename, debug=debug)


def usage(prog):
    print "Usage: %s [options] [file]" % prog
    return 0


def help():
    print "Options and Arguments:"
    print "  -d enable debug output"
    print "  -e evaluate the string"
    print "  -h display this help"
    print "  -i inspect interactively"
    print "  -v display the version"
    return 0


def version():
    print "%s %s" % (mio.__name__, mio.__version__)
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
    opts.eval = parse_arg("-e", argv)
    opts.help = parse_bool_arg("-h", argv)
    opts.inspect = parse_bool_arg("-i", argv)
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
        status = runfile(args[0], debug=opts.debug)
        return repl(debug=opts.debug) if opts.inspect else status
    elif opts.eval:
        return runsource(opts.eval)
    else:
        return repl(debug=opts.debug)


def target(driver, args):
    driver.exe_name = "bin/mio"
    return main, None


def jitpolicy(driver):
    return JitPolicy()


if __name__ == "__main__":
    main(sys.argv)
