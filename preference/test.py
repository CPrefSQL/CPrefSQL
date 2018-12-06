#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module for grammar testing
'''

import os
import sys
from pyparsing import ParseException

# Required to relative package imports
PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.realpath(os.path.join(PATH, '..')))


if __name__ == '__main__':
    from grammar.theory_grammar import TheoryGrammar
    from preference.rule import CPRule
    from preference.theory import CPTheory
    if len(sys.argv) != 2:
        exit(0)
    try:
        RULE_LIST = []
        FILE = open(sys.argv[1])
        FILE_TEXT = FILE.read()
        PARSED = TheoryGrammar.parse(FILE_TEXT)
        print 'Original string:'
        print FILE_TEXT
        if PARSED is not None:
            print ''
            print 'ParseResult object:'
            for num, parsed_rule in enumerate(PARSED):
                print('rule ', num, parsed_rule)
            print 'CP-Rules'
            for num, parsed_rule in enumerate(PARSED):
                cp_rule = CPRule(parsed_rule)
                print('cp-rule ', num, cp_rule)
                RULE_LIST.append(cp_rule)
        THEORY = CPTheory(RULE_LIST)
        print 'Consistent: ', THEORY.is_consistency()
    except ParseException as parse_exception:
        print 'Parse error:'
        print parse_exception.line
        print parse_exception
