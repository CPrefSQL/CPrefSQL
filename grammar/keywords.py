# -*- coding: utf-8 -*-
'''
Module to define keywords
'''

from pyparsing import Keyword

from grammar.symbols import AND_SYM, IF_SYM, THEN_SYM, BETTER_SYM

# Grammar keywords
AND_KEYWORD = Keyword(AND_SYM, caseless=True)
BETTER_KEYWORD = Keyword(BETTER_SYM, caseless=True)
IF_KEYWORD = Keyword(IF_SYM, caseless=True)
THEN_KEYWORD = Keyword(THEN_SYM, caseless=True)
