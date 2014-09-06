#!/usr/bin/env python


"""Usage: mio <filename>"""


import sys


from rpython.jit.codewriter.policy import JitPolicy
from rpython.rlib.streamio import open_file_as_stream
from pypy.objspace.std.bytesobject import string_escape_encode


from mio.lexer import lex


def main(argv):
    if not len(argv) == 2:
        print __doc__
        return 1

    filename = argv[1]
    f = open_file_as_stream(filename)
    source = f.readall()
    f.close()

    for token in lex(source):
        print "<Token (%s, %s)>" % (
            token.name,
            string_escape_encode(token.value, "'")
        )

    return 0


def target(driver, args):
    driver.exe_name = "bin/mio"
    return main, None


def jitpolicy(driver):
    return JitPolicy()


if __name__ == "__main__":
    main(sys.argv)
