# -*- coding: utf-8 -*-
'''
Module to manipulate intervals of values.


The intervals are stored as tuples.
The intervals are associated to comparisons as:
(A = x), (A <> x), (A < x), (A <= x), )A > x), (A >= x)
(x OP A OP x') where OP is < or <=
'''


from grammar.symbols import EQUAL_OP, DIFFERENT_OP, LESS_OP,\
    LESS_EQUAL_OP, GREATER_OP

# Values for infinity limits of intervals
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


def _equal_different_intersect(interval1, interval2):
    '''
    Check for overlap on equality and different comparisons
    '''
    # Check if intervals are the same
    if interval1 == interval2:
        return True
    # Check if interval1 is (v, <>, <>, v)
    if interval1[1] == DIFFERENT_OP:
        # Unique condition for no overlap
        # interval1  ------[ ]------
        # interval2        [X]
        if interval2[1] == EQUAL_OP and interval1[0] == interval2[0]:
            return False
        return True
    # Check if interval2 is (v, <>, <>, v)
    if interval2[1] == DIFFERENT_OP:
        # Unique condition for no overlap
        # interval2  ------[ ]------
        # interval1        [X]
        if interval1[1] == EQUAL_OP and interval1[0] == interval2[0]:
            return False
        return True
    return False


def _interval_intersect(interval1, interval2):
    '''
    Check if there is interval intersection
    '''
    # Check for overlap between = and <> operators
    if _equal_different_intersect(interval1, interval2):
        return True
    # interval1       [x] or [x]-------
    # interval2    |---------------|
    # or
    # interval1  ------[x] or [x]
    # interval2    |---------------|
    if (EQUAL_OP in interval1[1]
        and _is_inside_interval(interval1[0], interval2)) \
            or (EQUAL_OP in interval1[2]
                and _is_inside_interval(interval1[3], interval2)):
        return True
    # interval2       [x] or [x]-------
    # interval1    |---------------|
    # or
    # interval2  ------[x] or [x]
    # interval1    |---------------|
    if (EQUAL_OP in interval2[1]
        and _is_inside_interval(interval2[0], interval1)) \
        or (EQUAL_OP in interval2[2]
            and _is_inside_interval(interval2[3], interval1)):
        return True
    # interval1      |------|
    # interval2  |--------|
    if _before(interval1[0], interval2[3]) \
            and _after(interval1[3], interval2[0]):
        return True
    # interval2      |------|
    # interval1  |--------|
    if _before(interval2[0], interval1[3]) \
            and _after(interval2[3], interval1[0]):
        return True
    return False


def _after(value1, value2):
    '''
    Check if value2 is after value1
    '''
    # Check if value2 is +infinite (nothing can be after +infinite)
    if value2 == PLUS_INF:
        return False
    # Check if value2 is +infinite and value1 is not +infinite
    if value1 == PLUS_INF and value2 != PLUS_INF:
        return True
    if value1 == MINUS_INF:
        return False
    if value2 == MINUS_INF and value1 != MINUS_INF:
        return True
    return value1 > value2


def _before(value1, value2):
    '''
    Check if value1 appears before value 2
    '''
    # Check if value2 is -infinite (nothing can be before -infinite)
    if value2 == MINUS_INF:
        return False
    if value1 == MINUS_INF and value2 != MINUS_INF:
        return True
    if value1 == PLUS_INF:
        return False
    if value2 == PLUS_INF and value1 != PLUS_INF:
        return True

    return value1 < value2


def _after_left(value, interval):
    '''
    Check if value appears after left interval limit
    '''
    # Check if left limit is no -infinite and value is -infinite
    if interval[0] != MINUS_INF \
            and value == MINUS_INF:
        return False
    # Check if left limit is -infinite or value is +infinite
    # or value is after left limit
    if interval[0] == MINUS_INF \
            or value == PLUS_INF \
            or interval[0] < value \
            or (interval[0] <= value and
                EQUAL_OP in interval[1]):
        return True
    return False


def _before_right(value, interval):
    '''
    Check if value appears before right interval limit
    '''
    # Check if right limit is no +infinite and value is +infinite
    if interval[3] != PLUS_INF \
            and value == PLUS_INF:
        return False
    # Check if right limit is -infinite or value is +infinite
    # or value is before right limit
    if interval[3] == PLUS_INF \
            or value == MINUS_INF \
            or interval[3] > value \
            or (interval[3] >= value and
                EQUAL_OP in interval[2]):
        return True
    return False


def _is_inside_interval(value, interval):
    '''
    Check if a value is inside an interval
    '''
    # for intervals (v, <>, <>, v), only v is not in the interval
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


def split_neq_interval(interval):
    '''
        Split interval in the form ( Value, '<>', '<>', Value)
        to two intervals:
            ('-inf','<=', '<', Value)
            (Value, '<', '<=', '+inf')
    '''
    interval_list = []

    # verify if it's neq interval
    if (interval[1] == DIFFERENT_OP) and (interval[2] == DIFFERENT_OP):
        interval1 = (MINUS_INF, LESS_EQUAL_OP, LESS_OP, interval[0])
        interval2 = (interval[0], LESS_OP, LESS_EQUAL_OP, PLUS_INF)
        interval_list.append(interval1)
        interval_list.append(interval2)

    return interval_list


def _left_equal(interval1, interval2):
    """
    Check if 'interval1' left limit is equal 'interval2' left limit
    """
    if interval1[1] == interval2[1] and interval1[0] == interval2[0]:
        return True
    elif interval1[1] in ('=', '<=') and interval2[1] in ('=', '<=') \
            and interval1[0] == interval2[0]:
        return True
    else:
        return False


def _right_equal(interval1, interval2):
    """
    Check if 'interval1' right limit is equal 'interval2' right limit
    """
    if interval1[2] == interval2[2] and interval1[3] == interval2[3]:
        return True
    elif interval1[2] in ('=', '<=') and interval2[2] in ('=', '<=') \
            and interval1[3] == interval2[3]:
        return True
    else:
        return False


def _left_after(interval1, interval2):
    """
    Check if 'interval1' left limit is after 'interval2' left limit
    """
    # interval1: |---
    # interval2: <---
    if interval2[0] == MINUS_INF and interval1[0] != MINUS_INF:
        return True
    # interval1:  |---
    # interval2: |---
    elif interval2[1] in ('<', '<=') and interval1[1] in ('<', '<=', '=') \
            and interval2[0] < interval1[0]:
        return True
    # interval1: []---
    # interval2:  |---
    elif interval2[1] == '<=' and interval1[1] == '<' \
            and interval2[0] == interval1[0]:
        return True
    else:
        return False


def _right_before(interval1, interval2):
    """
    Check if 'interval1' right limit is before 'interval2' right limit
    """
    # interval1: ---|
    # interval2: --->
    if interval2[3] == PLUS_INF and interval1[3] != PLUS_INF:
        return True
    # interval1: ---|
    # interval2:  ---|
    elif interval2[2] in ('<', '<=') and interval1[2] in ('<', '<=', '=') \
            and interval2[3] > interval1[3]:
        return True
    # interval1: ---[]
    # interval2: ---|
    elif interval2[2] == '<=' and interval1[2] == '<' \
            and interval2[3] == interval1[3]:
        return True
    else:
        return False


def _right_after_equal_left(interval1, interval2):
    """
    Check if 'interval1' right limit is after or equal 'interval2' left limit
    """
    # interval1: ---|
    # interval2:  |---
    if interval1[3] != PLUS_INF and interval2[0] != MINUS_INF \
            and interval1[3] > interval2[0]:
        return True
    # interval1: ---|
    # interval2: <---
    elif interval1[3] != PLUS_INF and interval2[0] == MINUS_INF:
        return True
    # interval1: --->
    # interval2:  |---
    elif interval1[3] == PLUS_INF and interval2[0] != MINUS_INF:
        return True
    # interval1: ---|
    # interval2:    |---
    elif interval1[2] in ('<=', '=') and interval2[1] in ('=', '<=') \
            and interval1[3] == interval2[0]:
        return True
    else:
        return False


def split_interval(split_interval, fixed_interval):
    """
    Split 'split_interval' if 'fixed_interval' overlaps 'split_interval'
    """
    new_interval_list = []

    # Get part of 'fixed_interval' that overlaps 'split_interval'
    # First possibility, 'fixed_interval' inside
    # (at least one side) 'split_interval'
    # just copy fixed_interval

    #                   fixed_interval:   |--|
    #                   split_interval: |------|
    # split_interval' = fixed_interval:   |--|
    if _left_after(fixed_interval, split_interval) \
            and _right_before(fixed_interval, split_interval):
        new_interval_list.append(fixed_interval)

    #                   split_interval: |------|
    #                   fixed_interval: |--|
    # split_interval' = fixed_interval: |--|
    elif _left_equal(fixed_interval, split_interval) \
            and _right_before(fixed_interval, split_interval):
        new_interval_list.append(fixed_interval)
    #          fixed_interval:    |--|
    #          split_interval: |-----|
    # split_interval' = fixed_interval:    |--|
    elif _left_after(fixed_interval, split_interval) \
            and _right_equal(fixed_interval, split_interval):
        new_interval_list.append(fixed_interval)

    # Second possibility, 'fixed_interval' right limit
    # overlaps 'split_interval' left limit

    #  fixed_interval: ----|
    #  split_interval:  |-----
    # split_interval':  |--|
    elif _right_after_equal_left(fixed_interval, split_interval) \
            and _right_before(fixed_interval, split_interval):
        new_interval_list.append((split_interval[0], split_interval[1],
                                  fixed_interval[2], fixed_interval[3]))

    # Third possibility, 'fixed_interval' left limit
    # overlaps 'split_interval' right limit

    #  fixed_interval:  |-----
    #  split_interval: ----|
    # split_interval':  |--|
    elif _right_after_equal_left(split_interval, fixed_interval) \
            and _left_after(fixed_interval, split_interval):
        new_interval_list.append((fixed_interval[0], fixed_interval[1],
                                  split_interval[2], split_interval[3]))

    # Get part of 'split_interval' before 'fixed_interval'
    #  fixed_interval:   |----
    #  split_interval: -----|
    # split_interval': --|
    if _right_after_equal_left(split_interval, fixed_interval) \
            and _left_after(fixed_interval, split_interval):
        if fixed_interval[1] in ('=', '<='):
            new_interval_list.append((split_interval[0], split_interval[1],
                                      '<', fixed_interval[0]))
        else:
            new_interval_list.append((split_interval[0], split_interval[1],
                                      '<=', fixed_interval[0]))

    # Get part of 'split_interval' after 'fixed_interval'
    #  fixed_interval: ----|
    #  split_interval:  |-----
    # split_interval':     |--
    if _right_after_equal_left(fixed_interval, split_interval) \
            and _right_before(fixed_interval, split_interval):
        if fixed_interval[2] in ('=', '<='):
            new_interval_list.append((fixed_interval[3], '<',
                                      split_interval[2], split_interval[3]))
        else:
            new_interval_list.append((fixed_interval[3], '<=',
                                      split_interval[2], split_interval[3]))

    interval_list = []
    for interval in new_interval_list:
        if interval[0] == interval[3]:
            interval = (interval[0], '=', '=', interval[3])
        interval_list.append(interval)
    return interval_list
