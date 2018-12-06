# -*- coding: utf-8 -*-
'''
Module to define symbols
'''

# Preference keywords
TOP_SYM = 'TOP'
ACCORDING_SYM = 'ACCORDING'
TO_SYM = 'TO'
PREFERENCES_SYM = 'PREFERENCES'
IF_SYM = 'IF'
AND_SYM = 'AND'
THEN_SYM = 'THEN'
BETTER_SYM = 'BETTER'
PREFERENCES_SYM_SET = \
    set([TOP_SYM,
         ACCORDING_SYM,
         TO_SYM,
         PREFERENCES_SYM,
         IF_SYM,
         THEN_SYM,
         BETTER_SYM])


# Query keywords
# Select ... from ... where
SELECT_SYM = 'SELECT'
DISTINCT_SYM = 'DISTINCT'
FROM_SYM = 'FROM'
WHERE_SYM = 'WHERE'
GROUP_SYM = 'GROUP'
AS_SYM = 'AS'
NOT_SYM = 'NOT'
OR_SYM = 'OR'
BY_SYM = 'BY'
SIMPLE_QUERY_SYM_SET = \
    set([SELECT_SYM,
        DISTINCT_SYM,
        FROM_SYM,
        WHERE_SYM,
        GROUP_SYM,
        BY_SYM,
        AS_SYM,
        NOT_SYM,
        OR_SYM,
        AND_SYM]).union(PREFERENCES_SYM_SET)


# Bag
UNION_SYM = 'UNION'
INTERSECT_SYM = 'INTERSECT'
EXCEPT_SYM = 'EXCEPT'
BAG_SYM_SET = set([UNION_SYM, INTERSECT_SYM, EXCEPT_SYM])

QUERY_SYM_SET = SIMPLE_QUERY_SYM_SET.union(BAG_SYM_SET)

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

RESERVERD_SYM_SET = QUERY_SYM_SET


def is_reserved_word(word):
    '''
    Check if 'keyword' is a reserved keyword
    '''
    return word.upper() in RESERVERD_SYM_SET
