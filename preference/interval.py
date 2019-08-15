# -*- coding: utf-8 -*-
'''
Module to manipulate intervals of values.


The intervals are stored as tuples.
The intervals are associated to comparisons as:
(A = x), (A <> x), (A < x), (A <= x), )A > x), (A >= x)
(x OP A OP x') where OP is < or <=,
None represents infinity values
'''

from grammar.symbols import EQUAL_OP, DIFFERENT_OP, LESS_OP,\
    LESS_EQUAL_OP, GREATER_OP


MINUS_INF = float('-inf')
PLUS_INF = float('+inf')


def parse_interval(term):
    '''
    Parse a token term to interval
    '''
    # Check if parsed expression is a simple comparison
    if term.operator:
        # Comparisons: A = x, A <> x
        # Interval: (x, =, =, x), (x, <>, <> x)
        if term.operator in [EQUAL_OP, DIFFERENT_OP]:
            return (term.value, term.operator, term.operator, term.value)
        # Comparisons: A < x or A <= x
        # Intervals: (-inf, <=, <, x) or (-inf, <=, <=, x)
        elif term.operator in [LESS_OP, LESS_EQUAL_OP]:
            return (MINUS_INF, LESS_EQUAL_OP, term.operator, term.value)
        # Comparison: A > x
        # Interval: (x, <, <=, +inf)
        elif term.operator == GREATER_OP:
            return (term.value, LESS_OP, LESS_EQUAL_OP, PLUS_INF)
        # Comparison: A >= x
        # Interval: (x, <=, <=, +inf)
        return (term.value, LESS_EQUAL_OP, LESS_EQUAL_OP, PLUS_INF)
    # Comparisons: x OP A OP x'
    # Intervals: (x, OP, OP, x')
    return (term.left_value, term.left_operator,
            term.right_operator, term.right_value)


# def _interval_intersect(interval1, interval2):
#     '''
#     Check if there is interval intersection
#     '''
#     intersection = True
#     # Check if interval1 is (v, <>, <>, v) and interval2 is (v, =, =, v)
#     if interval1[1] == EQUAL_OP and interval2[1] == EQUAL_OP \
#             and interval1[0] != interval2[0]:
#         intersection = False
#     elif interval1[1] == DIFFERENT_OP and interval2[1] == EQUAL_OP \
#             and interval1[0] == interval2[0]:
#         intersection = False
#     # Check if interval1 is (v, =, =, v) and interval2 is (v, <>, <>, v)
#     elif interval1[1] == EQUAL_OP and interval2[1] == DIFFERENT_OP \
#             and interval1[0] == interval2[0]:
#         intersection = False
#     # Check if interval1 is (v, =, =, v)
#     # and interval2 is (v1, < or <=, < or <=, v2)
#     elif interval1[1] == EQUAL_OP \
#             and interval2[1] in [LESS_OP, LESS_EQUAL_OP] \
#             and not _is_inside_interval(interval1[0], interval2):
#         intersection = False
#     # Check if interval2 is (v, =, =, v)
#     # and interval1 is (v1, < or <=, < or <=, v2)
#     elif interval2[1] == EQUAL_OP \
#             and interval1[1] in [LESS_OP, LESS_EQUAL_OP] \
#             and not _is_inside_interval(interval2[0], interval1):
#         intersection = False
#     # Both intervals are (v1, < or <=, < or <=, v2)
#     elif interval1[1] == LESS_OP \
#             and interval2[2] in [LESS_OP, LESS_EQUAL_OP] \
#             and _before_left(interval2[0], interval1):
#         intersection = False
#     elif interval1[2] == LESS_OP \
#             and interval2[1] in [LESS_OP, LESS_EQUAL_OP] \
#             and _after_right(interval2[0], interval1):
#         intersection = False
#     elif interval2[1] == LESS_OP \
#             and interval1[2] in [LESS_OP, LESS_EQUAL_OP] \
#             and _before_left(interval1[0], interval2):
#         intersection = False
#     elif interval2[2] == LESS_OP \
#             and interval1[1] in [LESS_OP, LESS_EQUAL_OP] \
#             and _after_right(interval1[0], interval2):
#         intersection = False
#     elif interval1[1] == LESS_EQUAL_OP and interval1[2] == LESS_EQUAL_OP \
#             and interval2[1] == LESS_EQUAL_OP \
#             and interval2[2] == LESS_EQUAL_OP \
#             and not (_is_inside_interval(interval1[0], interval2)
#                      or _is_inside_interval(interval1[3], interval2)):
#         intersection = False

def _interval_intersect(interval1, interval2):
    '''
    Check if there is interval intersection
    '''
    # Check if intervals are the same
    if interval1 == interval2:
        return True
    if interval1[1] == DIFFERENT_OP and interval2[1] != EQUAL_OP:
        return True
    if interval2[1] == DIFFERENT_OP and interval1[1] != EQUAL_OP:
        return True
    # Check if interval1 is (v, <>, <>, v) and interval2 is (v, =, =, v)
    if interval1[1] == DIFFERENT_OP and interval2[1] == EQUAL_OP:
        return not interval1[0] == interval2[0]
    # Check if interval1 is (v, =, =, v) and interval2 is (v, <>, <>, v)
    if interval2[1] == DIFFERENT_OP and interval1[1] == EQUAL_OP:
        return not interval1[0] == interval2[0]
    if EQUAL_OP in interval1[1] \
            and _is_inside_interval(interval1[0], interval2):
        return True
    if EQUAL_OP in interval1[2] \
            and _is_inside_interval(interval1[3], interval2):
        return True
    if EQUAL_OP in interval2[1] \
            and _is_inside_interval(interval2[0], interval1):
        return True
    if EQUAL_OP in interval2[2] \
            and _is_inside_interval(interval2[3], interval1):
        return True
    if _before(interval1[0], interval2[3]) \
            and _after(interval1[3], interval2[0]):
        return True
    if _before(interval2[0], interval1[3]) \
            and _after(interval2[3], interval1[0]):
        return True
    return False


def _after(value1, value2):
    if value1 == PLUS_INF:
        return False
    if value2 == PLUS_INF and value1 != PLUS_INF:
        return True
    return value1 > value2


def _before(value1, value2):
    if value1 == MINUS_INF:
        return False
    if value2 == MINUS_INF and value1 != MINUS_INF:
        return True
    return value1 < value2


def _after_left(value, interval):
    '''
    Check if value is after left interval limit
    '''
    if interval[0] != MINUS_INF \
            and value == MINUS_INF:
        return False
    if interval[0] == MINUS_INF \
            or value == PLUS_INF \
            or interval[0] < value \
            or (interval[0] <= value and
                EQUAL_OP in interval[1]):
        return True
    return False


def _before_right(value, interval):
    '''
    Check if value is before right interval limit
    '''
    if interval[3] != PLUS_INF \
            and value == PLUS_INF:
        return False
    if interval[3] == PLUS_INF \
            or value == MINUS_INF \
            or interval[3] > value \
            or (interval[3] >= value and
                EQUAL_OP in interval[2]):
        return True
    return False


def _strict_after_left(value, interval):
    '''
    Check if value is after left interval limit
    '''
    if interval[0] != MINUS_INF \
            and value == MINUS_INF:
        return False
    if interval[0] == MINUS_INF \
            or value == PLUS_INF \
            or interval[0] < value:
        return True
    return False


def _strict_before_right(value, interval):
    '''
    Check if value is before right interval limit
    '''
    if interval[3] != PLUS_INF \
            and value == PLUS_INF:
        return False
    if interval[3] == PLUS_INF \
            or value == MINUS_INF \
            or interval[3] > value:
        return True
    return False


# def _before_left(value, interval):
#     '''
#     Check if value is before left interval limit
#     '''
#     if value is not None \
#             or value > interval[0] \
#             or (value == interval[0] and
#                 interval[1] == LESS_OP):
#         return False
#     return True
#
#
# def _after_right(value, interval):
#     '''
#     Check if value is after right interval limit
#     '''
#     if value is not None \
#             or value < interval[3] \
#             or (value == interval[3] and
#                 interval[2] == LESS_OP):
#         return False
#     return True


def _is_inside_interval(value, interval):
    '''
    Check if a value is inside an interval
    '''
    if interval[1] == DIFFERENT_OP and value != interval[0]:
        return True
    elif _after_left(value, interval) and _before_right(value, interval):
        return True
    return False


def _is_strict_inside_interval(value, interval):
    '''
    Check if a value is inside an interval
    '''
    if interval[1] == DIFFERENT_OP and value != interval[0]:
        return True
    elif _strict_after_left(value, interval) and _strict_before_right(value, interval):
        return True
    return False


def intersect(item1, item2):
    '''
    Check if there is interval or value intersection
    '''
    # Check if item1 is interval
    if isinstance(item1, tuple):
        # Check if item2 is interval
        if isinstance(item2, tuple):
            # Check if there is interval intersection (both intervals)
            return _interval_intersect(item1, item2)
        # Check if item2 is inside item1 (interval)
        return _is_inside_interval(item2, item1)
    # Check if item2 is interval
    elif isinstance(item2, tuple):
        # Check if item1 is inside item2 (interval)
        return _is_inside_interval(item1, item2)
    # Check if items are the same (both are none intervals)
    return item1 == item2


def get_str_predicate(attribute, interval):
    '''
    Get string for attribute and interval
    '''
    return str(interval[0]) + interval[1] + attribute + interval[2] + \
        str(interval[3])
