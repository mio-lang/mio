# Module:   parser
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Parser"""


from rply import Token, ParserGenerator
from pypy.objspace.std.bytesobject import string_escape_encode


from mio.ast import Message
from mio.tokens import TOKENS


pg = ParserGenerator(
    TOKENS.keys(),
    precedence=[
    ],
    cache_id=__name__
)


def isMessage(x):
    return isinstance(x, Message)


def isToken(x):
    return isinstance(x, Token)


def isList(x):
    return isinstance(x, list)


def isTuple(x):
    return isinstance(x, tuple)


def isString(x):
    return isinstance(x, str)


@pg.production("program : expressions")
def program(state, p):
    print "program:", p

    assert isMessage(p[0])

    return p[0]


@pg.production("expressions :")
def expressions(state, p):
    return Message("")


"""
@pg.production("expressions : expression expressions")
def expressions_expression_expressions(state, p):
    print "expressions:", p

    assert isMessage(p[0])
    assert isMessage(p[1])
    p[0].setnext(p[1])
    return p[0]


@pg.production("expression : message")
def expression(state, p):
    print "expression:", p
    assert isMessage(p[0])
    return p[0]


@pg.production("message : symbol")
def message_symbol(state, p):
    print "message_symbol:", p

    assert isMessage(p[0])
    return p[0]


@pg.production("message : arguments")
def message_arguments(state, p):
    print "message_arguments:", p

    assert isMessage(p[0])

    return p[0]


@pg.production("message : symbol arguments")
def message_symbol_arguments(state, p):
    print "message_symbol_arguments:", p

    assert isMessage(p[0])
    assert isMessage(p[1])

    p[0].setargs(p[1].getargs())

    return p[0]


@pg.production("arguments : T_LPAREN arguments_list T_RPAREN")
@pg.production("arguments : T_LBRACE arguments_list T_RBRACE")
@pg.production("arguments : T_LBRACKET arguments_list T_RBRACKET")
def arguments(state, p):
    print "arguments:", p

    assert isToken(p[0])
    assert isList(p[1])
    assert isToken(p[2])
    assert all(map(isMessage, p[1]))

    name = p[0].getstr() + p[2].getstr()
    args = p[1]

    return Message(name, args)


@pg.production("arguments_list :")
def arguments_list(state, p):
    print "arguments_list:", p

    assert len(p) == 0

    return []


@pg.production("arguments_list : expressions")
def arguments_list_expressions(state, p):
    print "arguments_list_expressions:", p

    assert isMessage(p[0])
    return [p[0]]


@pg.production("arguments_list : expressions T_COMMA arguments_list")
def arguments_list_expressions_t_comma_arguments_list(state, p):
    print "arguments_list_expressions_t_comma_arguments_list:", p

    assert isMessage(p[0])
    assert isToken(p[1])
    assert isList(p[2])
    p[2].insert(0, p[0])
    return p[2]


@pg.production("symbol : T_TERMINATOR")
@pg.production("symbol : T_IDENTIFIER")
@pg.production("symbol : T_OPERATOR")
@pg.production("symbol : T_NUMBER")
@pg.production("symbol : T_STRING")
@pg.production("symbol : T_COLON")
def symbol(state, p):
    print "symbol:", p

    assert isToken(p[0])

    name = p[0].getstr()
    value = parse_literal(name)

    return Message(name, value=value)
"""


@pg.error
def error(state, token):
    sourcepos = token.getsourcepos()

    if sourcepos is None:
        col, line = "?", "?"
    else:
        col, line = str(sourcepos.colno), str(sourcepos.lineno)

    raise ValueError(
        "Unexpected token <%s %s> at %s:%s:%s" % (
            token.gettokentype(), string_escape_encode(token.getstr(), "'"),
            state.filename, line, col
        )
    )


parser = pg.build()


class ParserState(object):

    def __init__(self, filename=None):
        self.filename = filename


def parse_literal(value):
    return value


def parse(tokens, filename=None):
    state = ParserState(filename)
    return parser.parse(tokens, state=state)
