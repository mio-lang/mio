# Module:   lexer
# Date:     6th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Lexer"""


from rply import LexerGenerator


from .tokens import TOKENS, IGNORES


lg = LexerGenerator()

for name, rule in TOKENS.iteritems():
    lg.add(name, rule)

for rule in IGNORES:
    lg.ignore(*rule)

# This has to be called outside a function because the parser must be generated
# in Python during translation, not in RPython during runtime.
lexer = lg.build()


def lex(text):
    """Scan text using the generated lexer.

    :param text: text to lex
    :type text: :class:`str`

    :return: parsed stream
    :rtype: :class:`rply.lexer.LexerStream`
    """

    return lexer.lex(text)
