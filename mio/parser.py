# Module:   parser
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Parser"""


from rply import ParserGenerator


from .ast import Message
from .tokens import TOKENS
from .errors import SyntaxError
from .rstringutils import string_escape_encode


pg = ParserGenerator(TOKENS.keys(), cache_id=__name__)


null = Message("")


@pg.production("program : expressions")
def program(state, p):
    return p[0]


@pg.production("expressions :")
def expressions(state, p):
    return null


@pg.production("expressions : expression expressions")
def expressions_expression_expressions(state, p):
    if p[1] != null:
        p[0].setnext(p[1])
    return p[0]


@pg.production("expression : terminator")
@pg.production("expression : message")
def expression(state, p):
    return p[0]


@pg.production("message : symbol")
def message_symbol(state, p):
    return p[0]


@pg.production("message : arguments")
def message_arguments(state, p):
    return p[0]


@pg.production("message : symbol arguments")
def message_symbol_arguments(state, p):
    p[0].setargs(p[1].getargs())
    return p[0]


@pg.production("arguments : T_LPAREN arguments_list T_RPAREN")
@pg.production("arguments : T_LBRACE arguments_list T_RBRACE")
@pg.production("arguments : T_LBRACKET arguments_list T_RBRACKET")
def arguments(state, p):
    name = p[0].getstr() + p[2].getstr()
    args = p[1].getargs()
    if args == [null]:
        args = []

    return Message(name, args)


@pg.production("arguments_list :")
def arguments_list(state, p):
    return null


@pg.production("arguments_list : expressions")
def arguments_list_expressions(state, p):
    return Message("", [p[0]])


@pg.production("arguments_list : expressions T_COMMA arguments_list")
def arguments_list_expressions_t_comma_arguments_list(state, p):
    args = [p[0]] + p[2].getargs()
    p[2].setargs(args)

    return p[2]


@pg.production("symbol : T_IDENTIFIER")
@pg.production("symbol : T_OPERATOR")
@pg.production("symbol : T_NUMBER")
@pg.production("symbol : T_STRING")
def symbol(state, p):
    name = p[0].getstr()
    value = name if p[0].gettokentype() in ("T_NUMBER", "T_STRING") else None

    return Message(name, value=value)


@pg.production("terminator : T_TERMINATOR")
def terminator(state, p):
    return Message(p[0].getstr())


@pg.error
def error(state, token):
    sourcepos = token.getsourcepos()

    if sourcepos is None:
        col, line = "?", "?"
    else:
        col, line = str(sourcepos.colno), str(sourcepos.lineno)

    raise SyntaxError(
        "Unexpected token <%s %s> at %s:%s:%s" % (
            token.gettokentype(), string_escape_encode(token.getstr(), "'"),
            state.filename, line, col
        )
    )


parser = pg.build()


class ParserState(object):

    def __init__(self, filename=None):
        self.filename = filename


def parse(tokens, filename=None):
    state = ParserState(filename)
    return parser.parse(tokens, state=state)
