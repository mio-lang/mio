#!/usr/bin/env python


"""Usage: test"""


import sys
from functools import wraps


def main(argv):
    d = {"a": 1, "b": 2}

    for k, v in d.iteritems():
        print k
        print v

    return 0


def target(driver, args):
    driver.exe_name = "bin/test"
    return main, None


if __name__ == "__main__":
    main(sys.argv)
