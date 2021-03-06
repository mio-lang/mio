# Module:   tokens
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Tokens"""


import re
from collections import OrderedDict


from rpython.rlib.rsre.rsre_re import escape


# Order does matter here! It indicates precedence.
TOKENS = OrderedDict()


operators = OrderedDict([
    ("**", 1), ("++", 1), ("--", 1),
    ("+=", 1), ("-=", 1), ("*=", 1), ("/=", 1),

    ("<<", 1), (">>", 1), ("==", 0),
    ("!=", 0), ("<=", 0), (">=", 0), ("..", 1),

    ("+", 1), ("-", 1), ("*", 1), ("/", 1), ("=", 1), ("<", 0), (">", 0),
    ("!", 0), ("%", 1), ("|", 0), ("^", 0), ("&", 0), ("?", 1), (":", 1),

    ("in", 0), ("is", 0), ("or", 0), ("and", 0), ("not", 0),

    ("return", 0), ("yield", 0),
    ("from", 1), ("import", 1), ("raise", 0), ("assert", 0),
])

strtpl = """
    ([bu])?
    {start:s}
    [^\\{quote:s}]*?
    (
    (   \\\\[\000-\377]
        |   {quote:s}
        (   \\\\[\000-\377]
        |   [^\\{quote:s}]
        |   {quote:s}
        (   \\\\[\000-\377]
            |   [^\\{quote:s}]
        )
        )
    )
    [^\\{quote:s}]*?
    )*?
    {end:s}
"""

quotes = [
    {"quote": "'", "start": "'''", "end": "'''"},
    {"quote": "\"", "start": "\"\"\"", "end": "\"\"\""},
    {"quote": "'", "start": "'", "end": "'"},
    {"quote": "\"", "start": "\"", "end": "\""}
]

strre = "".join(strtpl.split())
strre = "|".join([strre.format(**quote) for quote in quotes])
strre = strre.format(**quotes[3])


TOKENS["T_STRING"] = strre
TOKENS["T_NUMBER"] = r"(-?(0|([1-9][0-9]*))(\.[0-9]+)?([Ee]-?[0-9]+)?)"
TOKENS["T_OPERATOR"] = "|".join(map(escape, operators))
TOKENS["T_IDENTIFIER"] = r"[A-Za-z_][A-Za-z0-9_]*"
TOKENS["T_TERMINATOR"] = r"[;\n\r]"
TOKENS["T_LBRACKET"] = "\["
TOKENS["T_RBRACKET"] = "\]"
TOKENS["T_LPAREN"] = "\("
TOKENS["T_RPAREN"] = "\)"
TOKENS["T_LBRACE"] = "\{"
TOKENS["T_RBRACE"] = "\}"
TOKENS["T_COMMA"] = "\,"


IGNORES = [
    # Whitespace
    (r"[ \f\t\v]+",),

    # Python style comments
    (r"#[^\n\r]*", re.MULTILINE),
]
