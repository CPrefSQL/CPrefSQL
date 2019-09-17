#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module with new algorithms
'''

from preference.theory import build_cptheory
from preference.comparison import _is_record_valid_by_formula


def get_hifor_best(preference_text, record_list):
    '''
    Get best records according to CPTheory (formulas algorithm)

    A record is best if it is not dominated by any other record
    '''

    # build theory from preference text
    theory = build_cptheory(preference_text)

    # get preference list and max formulas
    preference_list, max_formulas = theory.get_preference_list()

    # search for the records with the lowest level
    t = []
    best_level = float("Inf")

    for rec in record_list:

        for level_list, formula_list in enumerate(preference_list):
            for index in formula_list:
                # if find lower level, discard old records and reset best level
                if _is_record_valid_by_formula(max_formulas[index], rec):

                    level = level_list
                    if level < best_level:
                        best_level = level
                        t = [rec]
                    elif level == best_level:
                        t.append(rec)

                    # when a match is found,
                    # there is no need to keep looking
                    # through the other formulas
                    break

    return t


def get_hifor_topk(preference_text,  record_list, k):
    '''
    Get k best records according to CPTheory (formulas algorithm)

    A record is best if it is not dominated by any other record
    '''

    # build theory from preference text
    theory = build_cptheory(preference_text)

    # get preference list and max formulas
    preference_list, max_formulas = theory.get_preference_list()

    # search for the records with the lowest level
    t = []

    for formula_list in preference_list:
        for index in formula_list:

            for rec in record_list:
                # if find lower level, discard old records and reset best level
                if _is_record_valid_by_formula(max_formulas[index], rec):
                    t.append(rec)

                    if len(t) >= k:
                        return t

    # less than k records were found, add more
    if len(t) < k:
        for rec in record_list:
            if rec not in t:
                t.append(rec)
                if len(t) >= k:
                    break

    return t
