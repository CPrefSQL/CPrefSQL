#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module for best algorithm testing
'''

import os
import sys
import sqlite3

# Required to relative package imports
PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.realpath(os.path.join(PATH, '..')))


if __name__ == '__main__':
    from algorithms.partition import get_best_partition, get_topk_partition

    if len(sys.argv) != 4:
        exit(0)
    PREF_FILE = open(sys.argv[1])
    PREF_TEXT = PREF_FILE.read()
    DATA_FILE = sys.argv[2]
    DATA_TABLE = sys.argv[3]
    REC_LIST = []
    print('\n\nPreferences:')
    print(PREF_TEXT)
    CON = sqlite3.connect(DATA_FILE)
    CON.row_factory = sqlite3.Row
    CURSOR = CON.cursor()
    CURSOR.execute('SELECT * FROM ' + DATA_TABLE + ';')
    print('\n\nInput records:')
    for rec in CURSOR.fetchall():
        REC_LIST.append(dict(rec))
        print(dict(rec))

    print('\n\nBest records:')
    BEST_LIST = get_best_partition(PREF_TEXT, REC_LIST)
    for rec in BEST_LIST:
        print(rec)

    REC_LIST = []
    CURSOR.execute('SELECT * FROM ' + DATA_TABLE + ';')
    print('\n\nInput records:')
    for rec in CURSOR.fetchall():
        REC_LIST.append(dict(rec))
        print(dict(rec))

    print('\n\nTop-3 records:')
    BEST_LIST = get_topk_partition(PREF_TEXT, REC_LIST, 3)
    for rec in BEST_LIST:
        print(rec)
