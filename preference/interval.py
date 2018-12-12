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
        # Intervals: (None, <=, <, x) or (None, <=, <=, x)
        elif term.operator in [LESS_OP, LESS_EQUAL_OP]:
            return (None, LESS_EQUAL_OP, term.operator, term.value)
        # Comparison: A > x
        # Interval: (x, <, <=, None)
        elif term.operator == GREATER_OP:
            return (term.value, LESS_OP, LESS_EQUAL_OP, None)
        # Comparison: A >= x
        # Interval: (x, <=, <=, None)
        return (term.value, LESS_EQUAL_OP, LESS_EQUAL_OP, None)
    # Comparisons: x OP A OP x'
    # Intervals: (x, OP, OP, x')
    return (term.left_value, term.left_operator,
            term.right_operator, term.right_value)


def _interval_intersect(interval1, interval2):
    '''
    Check if there is interval intersection
    '''
    intersection = True
    # Check both intervals are (A, =, =, v)
    if interval1[1] == EQUAL_OP and interval2[1] == EQUAL_OP \
            and interval1[0] != interval2[0]:
        intersection = False
    # Check if interval1 is (A, <>, <>, v) and interval2 is (A, =, =, v)
    elif interval1[1] == DIFFERENT_OP and interval2[1] == EQUAL_OP \
            and interval1[0] == interval2[0]:
        intersection = False
    # Check if interval1 is (A, =, =, v) and interval2 is (A, <>, <>, v)
    elif interval1[1] == EQUAL_OP and interval2[1] == DIFFERENT_OP \
            and interval2[0] == interval1[0]:
        intersection = False
    # Check if interval1 is (A, =, =, v)
    # and interval2 is (A, <, <=, None) or (A, <=, <=, None)
    elif interval1[1] == EQUAL_OP \
            and interval2[1] in [LESS_OP, LESS_EQUAL_OP] \
            and not _is_inside_interval(interval1[0], interval2):
        intersection = False
    # Check if interval2 is (A, =, =, v)
    # and interval1 is (A, <, <=, None) or (A, <=, <=, None)
    elif interval2[1] == EQUAL_OP \
            and interval1[1] in [LESS_OP, LESS_EQUAL_OP] \
            and not _is_inside_interval(interval2[0], interval1):
        intersection = False
    # Both intervals are (A, <=, <=, None) or (A, <=, <=, None)
    elif interval1[1] in [LESS_OP, LESS_EQUAL_OP] \
            and interval2[1] in [LESS_OP, LESS_EQUAL_OP]:
        # Sort intervals
        if interval2[0] < interval1[0]:
            interval1, interval2 = interval2, interval1
        if not _is_inside_interval(interval1[3], interval2):
            intersection = False
    return intersection


def _after_left(value, interval):
    '''
    Check if value is after left interval limit
    '''
    if interval[0] is None \
            or interval[0] < value \
            or (interval[0] <= value and
                EQUAL_OP in interval[1]):
        return True
    return False


def _before_right(value, interval):
    '''
    Check if value is before right interval limit
    '''
    if interval[3] is None \
            or interval[3] > value \
            or (interval[3] >= value and
                EQUAL_OP in interval[2]):
        return True
    return False


def _is_inside_interval(value, interval):
    '''
    Check if a value is inside an interval
    '''
    if interval[1] == DIFFERENT_OP and value != interval[0]:
        return True
    elif _after_left(value, interval) and _before_right(value, interval):
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
