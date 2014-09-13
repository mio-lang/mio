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


@pg.production("program : expressions")
def program(state, p):
    print "program:", p

    assert isList(p)
    assert map(isMessage, p)

    chain = p[0]

    next = chain
    for message in p[1:]:
        next.setnext(message)
        next = message

    return chain


@pg.production("expressions :")
@pg.production("expressions : expression expressions")
def expressions(state, p):
    print "expressions:", p

    if len(p) == 2:
        assert isMessage(p[0])
        if p[1] is not None:
            assert isMessage(p[1])
            p[0].setnext(p[1])
            return p[0]

        return p[0]
    elif len(p) == 1:
        return p[0]
    else:
        return Message("")


@pg.production("expression : message")
@pg.production("expression : terminator")
def expression(state, p):
    print "expression:", p
    assert isMessage(p[0])
    return p[0]


@pg.production("message : symbol")
@pg.production("message : arguments")
@pg.production("message : symbol arguments")
def message(state, p):
    print "message:", p

    if len(p) == 1:
        assert isMessage(p[0])
        return p[0]

    assert isMessage(p[0])
    assert isMessage(p[1])

    p[0].setargs([p[1]])

    return p[0]


@pg.production("arguments : T_LPAREN arguments_list T_RPAREN")
@pg.production("arguments : T_LBRACE arguments_list T_RBRACE")
@pg.production("arguments : T_LBRACKET arguments_list T_RBRACKET")
def arguments(state, p):
    print "arguments:", p

    if p[0].gettokentype() == "T_LPAREN":
        name = "()"
    elif p[0].gettokentype() == "T_LBRACE":
        name = "{}"
    elif p[0].gettokentype() == "T_LBRACKET":
        name = "[]"
    else:
        name = "??"

    assert isList(p[1])
    assert all(map(isMessage, p[1]))

    return Message(name, args=[p[1]])


@pg.production("arguments_list :")
@pg.production("arguments_list : expressions")
@pg.production("arguments_list : expressions T_COMMA arguments_list")
def arguments_list(state, p):
    print "arguments_list:", p

    if len(p) == 3:
        if isinstance(p[2], list):
            assert isList(p[2])
            assert isMessage(p[0])
            p[2].insert(0, p[0])
            return p[2]
        else:
            assert isMessage(p[0])
            assert isMessage(p[2])
            return [p[0], p[2]]
    elif len(p) == 1:
        assert isMessage(p[0])
        return [p[0]]
    else:
        return []


@pg.production("symbol : T_IDENTIFIER")
@pg.production("symbol : T_OPERATOR")
@pg.production("symbol : T_NUMBER")
@pg.production("symbol : T_STRING")
def symbol(state, p):
    print "symbol:", p

    assert isToken(p[0])

    name = p[0].getstr()
    value = parse_literal(name)

    return Message(name, value=value)


@pg.production("terminator : T_TERMINATOR")
def terminator(state, p):
    print "terminator:", p

    assert isToken(p[0])

    return Message(p[0].getstr())


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
