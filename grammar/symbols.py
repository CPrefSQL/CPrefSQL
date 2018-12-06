# -*- coding: utf-8 -*-
'''
Module to define symbols
'''

from pyparsing import Keyword


# Preference keywords
ACCORDING_SYM = 'ACCORDING'
TO_SYM = 'TO'
PREFERENCES_SYM = 'PREFERENCES'
IF_SYM = 'IF'
AND_SYM = 'AND'
THEN_SYM = 'THEN'
BETTER_SYM = 'BETTER'
PREFERENCES_SYM_SET = \
    set([
         ACCORDING_SYM,
         TO_SYM,
         PREFERENCES_SYM,
         IF_SYM,
         THEN_SYM,
         BETTER_SYM])

# Symbols
LEFT_BRA = '['
RIGHT_BRA = ']'
LEFT_PAR = '('
RIGHT_PAR = ')'
COMMA = ','
DOT = '.'
SEMICOLON = ';'
UNDERLINE = '_'
SYMBOLS_SET = set([LEFT_BRA,
                   RIGHT_BRA,
                   LEFT_PAR,
                   RIGHT_PAR,
                   COMMA,
                   DOT,
                   SEMICOLON,
                   UNDERLINE])

# Operators
LESS_OP = '<'
GREATER_OP = '>'
LESS_EQUAL_OP = '<='
GREATER_EQUAL_OP = '>='
EQUAL_OP = '='
DIFFERENT_OP = '<>'
COMPARISON_OP_SET = set([EQUAL_OP,
                         LESS_OP,
                         LESS_EQUAL_OP,
                         GREATER_OP,
                         GREATER_EQUAL_OP,
                         DIFFERENT_OP])
INTERVAL_OP_SET = set([LESS_OP, LESS_EQUAL_OP])


MINUS_OP = '-'


# Grammar keywords
AND_KEYWORD = Keyword(AND_SYM, caseless=True)
BETTER_KEYWORD = Keyword(BETTER_SYM, caseless=True)
IF_KEYWORD = Keyword(IF_SYM, caseless=True)
THEN_KEYWORD = Keyword(THEN_SYM, caseless=True)
