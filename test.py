#!/usr/bin/env python


"""Usage: test"""


import sys
from functools import wraps


def method(f):
    @wraps(f)
    def wrapper(*args):
        print 'Calling decorated function'
        return f(*args)
    return wrapper


@method
def foo(x, y):
    return x + y


def main(argv):
    print foo(1, 2)

    return 0


def target(driver, args):
    driver.exe_name = "bin/test"
    return main, None


if __name__ == "__main__":
    main(sys.argv)
