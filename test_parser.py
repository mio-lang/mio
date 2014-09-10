#!/usr/bin/env python

from mio.lexer import lex
from mio.parser import parse


def test(s):
    return parse(lex(s))
