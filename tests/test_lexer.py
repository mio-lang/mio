# -*- encoding: utf-8 -*-


import pytest


from rply.token import Token


from mio.lexer import lex


@pytest.mark.parametrize("source,expected", [
    ("1",       Token("T_NUMBER", "1")),
    ("-1",      Token("T_NUMBER", "-1")),
    ("1e3",     Token("T_NUMBER", "1e3")),
    ("1E3",     Token("T_NUMBER", "1E3")),
    ("1e-3",    Token("T_NUMBER", "1e-3")),
    ("1E-3",    Token("T_NUMBER", "1E-3")),
    ("-1e3",    Token("T_NUMBER", "-1e3")),
    ("-1E3",    Token("T_NUMBER", "-1E3")),
    ("-1e-3",   Token("T_NUMBER", "-1e-3")),
    ("-1E-3",   Token("T_NUMBER", "-1E-3")),
    ("1.0",     Token("T_NUMBER", "1.0")),
    ("-1.0",    Token("T_NUMBER", "-1.0")),
    ("1.0e3",   Token("T_NUMBER", "1.0e3")),
    ("1.0E3",   Token("T_NUMBER", "1.0E3")),
    ("1.0e-3",  Token("T_NUMBER", "1.0e-3")),
    ("1.0E-3",  Token("T_NUMBER", "1.0E-3")),
    ("-1.0e3",  Token("T_NUMBER", "-1.0e3")),
    ("-1.0E3",  Token("T_NUMBER", "-1.0E3")),
    ("-1.0e-3", Token("T_NUMBER", "-1.0e-3")),
    ("-1.0E-3", Token("T_NUMBER", "-1.0E-3")),
])
def test_number(source, expected):
    actual = list(lex(source))
    assert actual
    assert actual[0] == expected


@pytest.mark.parametrize("source,expected", [
    ("'s'",             Token("T_STRING", "'s'")),
    ("'''s'''",         Token("T_STRING", "'''s'''")),
    ("\"s\"",           Token("T_STRING", "\"s\"")),
    ("\"\"\"s\"\"\"",   Token("T_STRING", "\"\"\"s\"\"\"")),
])
def test_string(source, expected):
    actual = list(lex(source))
    assert actual
    assert actual[0] == expected


@pytest.mark.parametrize("source,expected", [
    ("**", Token("T_OPERATOR", "**")),  ("++", Token("T_OPERATOR", "++")),
    ("--", Token("T_OPERATOR", "--")),  ("+=", Token("T_OPERATOR", "+=")),
    ("-=", Token("T_OPERATOR", "-=")),  ("*=", Token("T_OPERATOR", "*=")),
    ("/=", Token("T_OPERATOR", "/=")),  ("<<", Token("T_OPERATOR", "<<")),
    (">>", Token("T_OPERATOR", ">>")),  ("==", Token("T_OPERATOR", "==")),
    ("!=", Token("T_OPERATOR", "!=")),  ("<=", Token("T_OPERATOR", "<=")),
    (">=", Token("T_OPERATOR", ">=")),  ("..", Token("T_OPERATOR", "..")),
    ("+", Token("T_OPERATOR", "+")),    ("-", Token("T_OPERATOR", "-")),
    ("*", Token("T_OPERATOR", "*")),    ("/", Token("T_OPERATOR", "/")),
    ("=", Token("T_OPERATOR", "=")),    ("<", Token("T_OPERATOR", "<")),
    (">", Token("T_OPERATOR", ">")),    ("!", Token("T_OPERATOR", "!")),
    ("%", Token("T_OPERATOR", "%")),    ("|", Token("T_OPERATOR", "|")),
    ("^", Token("T_OPERATOR", "^")),    ("&", Token("T_OPERATOR", "&")),
    ("?", Token("T_OPERATOR", "?")),    (":", Token("T_OPERATOR", ":")),
    ("in", Token("T_OPERATOR", "in")),  ("is", Token("T_OPERATOR", "is")),
    ("or", Token("T_OPERATOR", "or")),  ("and", Token("T_OPERATOR", "and")),
    ("not", Token("T_OPERATOR", "not")),
    ("from", Token("T_OPERATOR", "from")),
    ("yield", Token("T_OPERATOR", "yield")),
    ("raise", Token("T_OPERATOR", "raise")),
    ("return", Token("T_OPERATOR", "return")),
    ("import", Token("T_OPERATOR", "import")),
    ("assert", Token("T_OPERATOR", "assert")),
])
def test_operators(source, expected):
    actual = list(lex(source))
    assert actual
    assert actual[0] == expected
