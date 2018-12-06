# -*- coding: utf-8 -*-
'''
Module for parsed structures
'''
# StreamPref import
from preference.interval import parse_interval, get_str_predicate


class ParsedPredicate(object):
    '''
    Class to represent parsed predicates
    '''

    def __init__(self, term):
        self._attribute = term.attribute
        self._interval = parse_interval(term)

    def __str__(self):
        return get_str_predicate(self._attribute, self._interval)
#         predicate_str = ''
#         if self._interval[0] is not None:
#             predicate_str += str(self._interval[0])
#         else:
#             predicate_str += '-INF'
#         predicate_str += ' ' + self._interval[1] + \
#             ' ' + str(self._attribute) + ' ' + \
#             self._interval[2] + ' '
#         if self._interval[3] is not None:
#             predicate_str += str(self._interval[3])
#         else:
#             predicate_str += '+INF'
#         return '({p})'.format(p=predicate_str)

    def __repr__(self):
        return self.__str__()

    def get_attribute(self):
        '''
        Return the predicate attribute
        '''
        return self._attribute

    def get_interval(self):
        '''
        Return the predicate interval
        '''
        return self._interval


# class ParsedRule(object):
#     '''
#     Class to represent a cp-rules
#     '''
#     def __init__(self, parsed_term):
#         self._condition_list = []
#         self._best = parsed_term.preference.best
#         self._worst = parsed_term.preference.worst
#         self._indifferent_list = []
#         if parsed_term.condition:
#             self._condition_list = parsed_term.condition
#         if parsed_term.indifferent:
#             self._indifferent_list = parsed_term.indifferent
#
#     def __str__(self):
#         rule_str = ''
#         if self._condition_list:
#             rule_str = 'IF' + ' ' + str(self._condition_list) + \
#                 ' ' + 'THEN' + ' '
#         rule_str += str(self._best) + ' BETTER ' + str(self._worst)
#         if self._indifferent_list:
#             rule_str += ' ' + 'INDIFF(' + \
#                 str(self._indifferent_list) + ')'
#         return 'RULE({c})'.format(c=rule_str)
#
#     def __repr__(self):
#         return self.__str__()
#
#     def get_condition_list(self):
#         '''
#         Return condition list
#         '''
#         return self._condition_list
#
#     def get_best_interval(self):
#         '''
#         Return best values
#         '''
#         return self._best
#
#     def get_worst_interval(self):
#         '''
#         Return worst values
#         '''
#         return self._worst
#
#     def get_indifferent_list(self):
#         '''
#         Return indifferent attribute list
#         '''
#         return self._indifferent_list
