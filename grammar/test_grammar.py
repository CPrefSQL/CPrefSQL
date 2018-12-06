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

# Check if file is executed as a program
if __name__ == '__main__':
    from grammar.theory_grammar import TheoryGrammar
    if len(sys.argv) != 2:
        exit(0)
    try:
        FILE = open(sys.argv[1])
        FILE_TEXT = FILE.read()
        PARSED = TheoryGrammar.parse(FILE_TEXT)
        print 'Original string:'
        print FILE_TEXT
        print 'Parsed:'
        print PARSED
        if PARSED is not None:
            print ''
            print 'ParseResult object:'
            for num, cprule in enumerate(PARSED):
                print('rule ', num, cprule)
    except ParseException as parse_exception:
        print 'Parse error:'
        print parse_exception.line
        print parse_exception
