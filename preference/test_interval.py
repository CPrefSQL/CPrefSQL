#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module for interval overlap test
'''

import os
import sys


# Required to relative package imports
PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.realpath(os.path.join(PATH, '..')))


if __name__ == '__main__':
    from preference.interval import intersect, get_str_predicate
    # Interval list
    INTERV_LIST = []
    # Value list
    VAL_LIST = [10, 20, 30, 40]
    # Equality operator
    EQUAL_OP_LIST = ['=', '<>']
    # Interval operator
    INTERV_OP_LIST = ['<', '<=']
    # Generate equality comparisons
    for VAL in VAL_LIST:
        for OP in EQUAL_OP_LIST:
            INTERV = (VAL, OP, OP, VAL)
            INTERV_LIST.append(INTERV)
    # Generate intervals comparisons
    for VAL1 in VAL_LIST:
        for OP1 in INTERV_OP_LIST:
            for OP2 in INTERV_OP_LIST:
                for VAL2 in VAL_LIST:
                    if VAL1 < VAL2:
                        INTERV = (VAL1, OP1, OP2, VAL2)
                        INTERV_LIST.append(INTERV)
    # Generate intervals having infinity limits
    for VAL in VAL_LIST:
        for OP in INTERV_OP_LIST:
            INTERV = (VAL, OP, '<=', float('inf'))
            INTERV_LIST.append(INTERV)
            INTERV = (float('-inf'), '<=', OP, VAL)
            INTERV_LIST.append(INTERV)
    INTERV_LIST.append((float('-inf'), '<=', '<=', float('inf')))
    # Print intersection (overlap) for each pair of intervals
    for INTERV1 in INTERV_LIST:
        for INTERV2 in INTERV_LIST:
            print(get_str_predicate('A', INTERV1),
                  get_str_predicate('A', INTERV2),
                  intersect(INTERV1, INTERV2))
