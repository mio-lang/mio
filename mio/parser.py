# Module:   parser
# Date:     7th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Parser"""


from rply import ParserGenerator


from .tokens import TOKENS
from .objects import Message


print TOKENS.keys()

pg = ParserGenerator(TOKENS.keys(), cache_id=__name__)


@pg.production("expression : terminator")
def expression(p):
    return p[0]


@pg.production("terminator : T_TERMINATOR")
def terminator(p):
    return Message(p[0].getstr())


@pg.error
def error(token):
    raise ValueError(
        "Ran into a %s where it wasn't expected" % token.gettokentype()
    )


parser = pg.build()


def parse(tokens):
    return parser.parse(tokens)
