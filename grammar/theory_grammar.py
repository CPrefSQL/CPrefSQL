# -*- coding: utf-8 -*-
'''
Module for conditional preference theory grammar
'''

from pyparsing import Suppress, Optional, delimitedList, Group, \
    ParseException
from grammar.basic import predicate_term, identifier_token
from grammar.symbols import GREATER_OP, IF_KEYWORD, AND_KEYWORD, \
    THEN_KEYWORD, BETTER_KEYWORD
from grammar.symbols import LEFT_BRA, RIGHT_BRA, LEFT_PAR, \
    RIGHT_PAR, COMMA


class TheoryGrammar(object):
    '''
    Class for cp-theory grammar

    <theory-grammar> ::= <rule-term> {'AND' <rule-term>}*
    <rule-term> ::= [<antecedent>] <preference> [<indifferent-list>]
    <condition-term> ::= 'IF' <predicate> {'AND' <predicate>}* 'THEN'
    <preference-term> ::=
        <predicate> 'BETTER' <predicate>' |
        <predicate> '>' <predicate>
    <indifferent-list> ::=
        '[' <attribute> (',' <attribute>)* ']' |
        '(' <attribute> (',' <attribute>)* ')'
    <predicate-term> ::=
        <attribute> {'<' | '<=' | '>' | '>=' | '=' | '<>'} <value> |
        <value> {'<' | '<='} <attribute> {'<' | '<='} <value>
    '''

    @classmethod
    def grammar(cls):
        '''
        Return grammar for cp-theories
        '''
        rule = rule_term()
        grammar = delimitedList(rule, AND_KEYWORD)
        return grammar

    @classmethod
    def parse(cls, string):
        '''Parse a string using the grammar'''
        try:
            parsed_cql = cls.grammar().parseString(string, parseAll=True)
            return parsed_cql
        except ParseException as p_e:
            print('Invalid code: %s', string)
            print('Invalid line: %s', p_e.line)
            print('Parsing error: %s', p_e)
            return None


def rule_term():
    '''
    Grammar for cp-rules

    [<condition>] <preference> [<indifferent-list>]
    '''
    condition = condition_term()
    preference = preference_term()
    indiff_list = indifferent_list()
    rule = Group(
                 Optional(condition).setResultsName('condition') +
                 preference +
                 Optional(indiff_list).setResultsName('indifferent')
                 )
    return rule


def condition_term():
    '''
    Grammar for condition term

    'IF' <predicate> {'AND' <predicate>}* 'THEN'
    '''
    predicate = predicate_term()
    condition = Group(Suppress(IF_KEYWORD) +
                      delimitedList(predicate, AND_KEYWORD) +
                      Suppress(THEN_KEYWORD))
    condition.setParseAction(lambda t: t[0].asList())
    return condition


def preference_term():
    '''
    Grammar for preference term

    <predicate> 'BETTER' <predicate>'
    <predicate> '>' <predicate>
    '''
    predicate = predicate_term()
    preference = predicate.setResultsName('best') + \
        Suppress(BETTER_KEYWORD | GREATER_OP) + \
        predicate.setResultsName('worst')
    return preference


def indifferent_list():
    '''
    Grammar for list of indifferent attributes

    '[' <attribute> (, <attribute>)* ']'
    '(' <attribute> (, <attribute>)* ')'
    '''
    att_term = identifier_token()
    indiff_par = Suppress(LEFT_PAR) + \
        delimitedList(att_term, COMMA) + \
        Suppress(RIGHT_PAR)
    indiff_bra = Suppress(LEFT_BRA) + \
        delimitedList(att_term, COMMA) + \
        Suppress(RIGHT_BRA)
    indiff_list = Group(indiff_par | indiff_bra)
    indiff_list.setParseAction(lambda t: t[0].asList())
    return indiff_list
