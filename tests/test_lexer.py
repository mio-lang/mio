# -*- encoding: utf-8 -*-


import pytest


from rply.token import Token


from mio.lexer import lex


@pytest.mark.parametrize("source,expected", [
    ("1",       [Token("T_NUMBER", "1")]),
    ("-1",      [Token("T_NUMBER", "-1")]),
    ("1e3",     [Token("T_NUMBER", "1e3")]),
    ("1E3",     [Token("T_NUMBER", "1E3")]),
    ("1e-3",    [Token("T_NUMBER", "1e-3")]),
    ("1E-3",    [Token("T_NUMBER", "1E-3")]),
    ("-1e3",    [Token("T_NUMBER", "-1e3")]),
    ("-1E3",    [Token("T_NUMBER", "-1E3")]),
    ("-1e-3",   [Token("T_NUMBER", "-1e-3")]),
    ("-1E-3",   [Token("T_NUMBER", "-1E-3")]),
    ("1.0",     [Token("T_NUMBER", "1.0")]),
    ("-1.0",    [Token("T_NUMBER", "-1.0")]),
    ("1.0e3",   [Token("T_NUMBER", "1.0e3")]),
    ("1.0E3",   [Token("T_NUMBER", "1.0E3")]),
    ("1.0e-3",  [Token("T_NUMBER", "1.0e-3")]),
    ("1.0E-3",  [Token("T_NUMBER", "1.0E-3")]),
    ("-1.0e3",  [Token("T_NUMBER", "-1.0e3")]),
    ("-1.0E3",  [Token("T_NUMBER", "-1.0E3")]),
    ("-1.0e-3", [Token("T_NUMBER", "-1.0e-3")]),
    ("-1.0E-3", [Token("T_NUMBER", "-1.0E-3")]),
])
def test_number(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("'s'",             [Token("T_STRING", "'s'")]),
    ("'''s'''",         [Token("T_STRING", "'''s'''")]),
    ("\"s\"",           [Token("T_STRING", "\"s\"")]),
    ("\"\"\"s\"\"\"",   [Token("T_STRING", "\"\"\"s\"\"\"")]),
])
def test_string(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    # double character operators
    ("**", [Token("T_OPERATOR", "**")]),  ("++", [Token("T_OPERATOR", "++")]),
    ("--", [Token("T_OPERATOR", "--")]),  ("+=", [Token("T_OPERATOR", "+=")]),
    ("-=", [Token("T_OPERATOR", "-=")]),  ("*=", [Token("T_OPERATOR", "*=")]),
    ("/=", [Token("T_OPERATOR", "/=")]),  ("<<", [Token("T_OPERATOR", "<<")]),
    (">>", [Token("T_OPERATOR", ">>")]),  ("==", [Token("T_OPERATOR", "==")]),
    ("!=", [Token("T_OPERATOR", "!=")]),  ("<=", [Token("T_OPERATOR", "<=")]),
    (">=", [Token("T_OPERATOR", ">=")]),  ("..", [Token("T_OPERATOR", "..")]),

    # single character operators
    ("+", [Token("T_OPERATOR", "+")]),    ("-", [Token("T_OPERATOR", "-")]),
    ("*", [Token("T_OPERATOR", "*")]),    ("/", [Token("T_OPERATOR", "/")]),
    ("=", [Token("T_OPERATOR", "=")]),    ("<", [Token("T_OPERATOR", "<")]),
    (">", [Token("T_OPERATOR", ">")]),    ("!", [Token("T_OPERATOR", "!")]),
    ("%", [Token("T_OPERATOR", "%")]),    ("|", [Token("T_OPERATOR", "|")]),
    ("^", [Token("T_OPERATOR", "^")]),    ("&", [Token("T_OPERATOR", "&")]),
    ("?", [Token("T_OPERATOR", "?")]),    (":", [Token("T_OPERATOR", ":")]),

    # logical worded operators
    ("in",      [Token("T_OPERATOR", "in")]),
    ("is",      [Token("T_OPERATOR", "is")]),
    ("or",      [Token("T_OPERATOR", "or")]),
    ("and",     [Token("T_OPERATOR", "and")]),
    ("not",     [Token("T_OPERATOR", "not")]),

    # special purpose operators
    ("from",    [Token("T_OPERATOR", "from")]),
    ("yield",   [Token("T_OPERATOR", "yield")]),
    ("raise",   [Token("T_OPERATOR", "raise")]),
    ("return",  [Token("T_OPERATOR", "return")]),
    ("import",  [Token("T_OPERATOR", "import")]),
    ("assert",  [Token("T_OPERATOR", "assert")]),
])
def test_operators(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("foo",     [Token("T_IDENTIFIER", "foo")]),
    ("foo1",    [Token("T_IDENTIFIER", "foo1")]),
    ("_foo",    [Token("T_IDENTIFIER", "_foo")]),
    ("Foo",     [Token("T_IDENTIFIER", "Foo")]),
    ("Foo1",    [Token("T_IDENTIFIER", "Foo1")]),
    ("_Foo",    [Token("T_IDENTIFIER", "_Foo")]),
    ("FOO",     [Token("T_IDENTIFIER", "FOO")]),
    ("FOO1",    [Token("T_IDENTIFIER", "FOO1")]),
    ("_FOO",    [Token("T_IDENTIFIER", "_FOO")]),
])
def test_identifier(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("\r",  [Token("T_TERMINATOR", "\r")]),
    ("\n",  [Token("T_TERMINATOR", "\n")]),
    (";",   [Token("T_TERMINATOR", ";")]),
])
def test_terminator(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("[",   [Token("T_LBRACKET", "[")]),
    ("]",   [Token("T_RBRACKET", "]")]),
])
def test_brackets(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("(",   [Token("T_LPAREN", "(")]),
    (")",   [Token("T_RPAREN", ")")]),
])
def test_parens(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("{",   [Token("T_LBRACE", "{")]),
    ("}",   [Token("T_RBRACE", "}")]),
])
def test_braces(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    (",", [Token("T_COMMA", ",")]),
])
def test_comma(source, expected):
    actual = list(lex(source))
    assert actual == expected


@pytest.mark.parametrize("source,expected", [
    ("",        []),
    (" ",       []),
    ("\f",      []),
    ("\t",      []),
    ("\v",      []),
    (" \f\t\v", []),
    ("#",       []),
    ("#foo",    []),
    (
        "#foo\nbar",
        [
            Token("T_TERMINATOR", "\n"),
            Token("T_IDENTIFIER", "bar")
        ]
    ),
])
def test_ignores(source, expected):
    actual = list(lex(source))
    assert actual == expected
