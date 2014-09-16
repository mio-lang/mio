# -*- encoding: utf-8 -*-


import pytest


from mio.lexer import lex
from mio.ast import Message
from mio.parser import parse


@pytest.mark.parametrize("source,message", [
    ("1", Message("1", value="1")),
    ("1.0", Message("1.0", value="1.0"))
])
def test_parse_numbers(source, message):
    # XXX: The parser is currently wrong here.
    parsed = parse(lex(source))
    assert parsed == message
