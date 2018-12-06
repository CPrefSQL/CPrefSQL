# -*- coding: utf-8 -*-
'''
Module for basic grammar used by others grammars
'''

# PyParsing import
from pyparsing import Suppress, Word, alphas, alphanums, \
    oneOf, nums, Optional, sglQuotedString, Combine

from grammar.symbols import MINUS_OP, COMPARISON_OP_SET
from grammar.parsed import ParsedPredicate


def identifier_token():
    '''
    Grammar for identifiers

    {[A-Z]|[a-z]|_)([A-Z]|[a-z]|[0-9]|_}*
    '''
    from grammar.symbols import UNDERLINE
    # Identifier begin with letter and have letters, numbers or underline
    identifier_tok = Word(alphas + UNDERLINE, alphanums + UNDERLINE)
    # Convert identifier to upper case
    identifier_tok.setParseAction(lambda t: t[0].upper())
    return identifier_tok


def string_value():
    '''
    Grammar for string values
    '''
    string_token = sglQuotedString
    string_token.setParseAction(lambda t: t[0][1:-1])
    return string_token


def float_value():
    '''
    Grammar for float values
    '''
    from grammar.symbols import DOT
    float_t = Combine(Optional(MINUS_OP) + Word(nums) + DOT + Word(nums))
    float_t.setParseAction(lambda t: float(t[0]))
    return float_t


def integer_value():
    '''
    Grammar for integer numbers
    '''
    integer_t = Combine(Optional(MINUS_OP) + Word(nums))
    integer_t.setParseAction(lambda t: int(t[0]))
    return integer_t


def value_term():
    '''
    Grammar for value tokens
    A value is an integer, a float or a string
    '''
    integer_tok = integer_value()
    integer_tok.setParseAction(lambda t: int(t[0]))
    float_token = float_value()
    float_token.setParseAction(lambda t: float(t[0]))
    string_tok = string_value()
    value_tok = (string_tok | float_token | integer_tok)
    return value_tok


def predicate_term():
    '''
    Grammar for predicates

    <attribute> {'<' | '<=' | '>' | '>=' | '=' | '<>'} <value>
    <value> {'<' | '<='} <attribute> {'<' | '<='} <value>
    '''
    from grammar.symbols import LEFT_PAR, RIGHT_PAR, \
        INTERVAL_OP_SET
    # Interval and comparison operators
    interval_op = oneOf(list(INTERVAL_OP_SET))
    comparison_op = oneOf(list(COMPARISON_OP_SET))
    value_tok = value_term()
    att_term = identifier_token()
    # Interval predicate
    interval_term = value_tok.setResultsName('left_value') + \
        interval_op.setResultsName('left_operator') + \
        att_term.setResultsName('attribute') + \
        interval_op.setResultsName('right_operator') + \
        value_tok.setResultsName('right_value')
    # Comparison predicate
    comparison_term = att_term.setResultsName('attribute') + \
        comparison_op.setResultsName('operator') + \
        value_tok.setResultsName('value')
    # Predicate is interval or comparison
    simple_predicate_term = interval_term | comparison_term
    pred_term = simple_predicate_term | \
        Suppress(LEFT_PAR) + simple_predicate_term + Suppress(RIGHT_PAR)
    pred_term.setParseAction(ParsedPredicate)
    return pred_term
