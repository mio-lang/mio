# -*- encoding: utf-8 -*-


import pytest


from mio.lexer import lex
from mio.ast import Message
from mio.parser import parse


@pytest.mark.parametrize("source,expected", [
    ("+",       Message("+")),
    (";",       Message(";")),
    ("\r",      Message("\r")),
    ("\n",      Message("\n")),
    ("foo",     Message("foo")),
    ("1",       Message("1", value="1")),
    ("\"s\"",   Message("\"s\"", value="\"s\"")),
])
def test_parse_message(source, expected):
    actual = parse(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("(1)",         Message("()", [Message("1", value="1")])),
    ("(1, 2, 3)",   Message("()", [Message("1", value="1"), Message("2", value="2"), Message("3", value="3")])),  # noqa
])
def test_parse_arguments(source, expected):
    actual = parse(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("foo(1)",         Message("foo", [Message("1", value="1")])),
    ("foo(1, 2, 3)",   Message("foo", [Message("1", value="1"), Message("2", value="2"), Message("3", value="3")])),  # noqa
])
def test_parse_message_with_arguments(source, expected):
    actual = parse(lex(source))
    assert actual == expected


def test_parse_expressions():
    source = "foo = method(a, b, return a + b); print(foo(1, 2))"

    m = Message("foo")
    m.setnext(Message("="))
    args = [Message("a"), Message("b")]
    args.append(Message("return"))
    args[-1].setnext(Message("a"))
    args[-1].setnext(Message("+"))
    args[-1].setnext(Message("B"))
    m.setnext(Message("method", args))
    m.setnext(Message(";"))
    m.setnext(Message("print"))
    args = [Message("1", value="1"), Message("2", value="2")]
    m.setnext(Message("foo", args))

    expected = m

    actual = parse(lex(source))

    assert actual == expected
