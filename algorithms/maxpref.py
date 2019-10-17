#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module with new algorithms
'''

from preference.theory import build_cptheory
from preference.comparison import _is_record_valid_by_formula


def get_maxpref_best(preference_text, record_list):
    '''
    Get best (maximal) records according to CPTheory (MaxPref semantic)

    A record is maximal if it is satisfies a formula F and do not exist
    other record satisfied by formulas better than F
    '''

    # Build theory from preference text
    theory = build_cptheory(preference_text)

    # Get maximal formulas and sorted formula list
    max_formulas = theory.get_max_formulas()
    sorted_list = theory.get_sorted_formulas()

    # List of records to be returned
    result_list = []
    # Current formula level (anyone is smaller then infinity)
    current_level = float("Inf")

    # For each input record
    for rec in record_list:
        # Suppose no level changes
        level_change = False 
        # For each sub_list of sorted formulas
        for formula_level, formula_list in enumerate(sorted_list):
            # For each formula in current formula level
            for formula_id in formula_list:
                # If record is satisfied by current formula
                if _is_record_valid_by_formula(max_formulas[formula_id], rec):
                    # If formula level is lower than current level
                    if formula_level < current_level:
                        # Change current level to formula level
                        level_change = True
                        current_level = formula_level
                        # Create a new result list
                        result_list = [rec]
                    # If formula level is equal to current level
                    elif formula_level == current_level:
                        # Append record into current list
                        result_list.append(rec)
                    # No need to search for other formulas
                    break
        # If there is level change, we prune the sorted list
        # We don't need formulas with higher levels
        if level_change:
            sorted_list = sorted_list[:current_level+1]
    # If no one record match with the formulas, we return all input records
    if len(result_list) == 0:
        return record_list
    return result_list


def get_hifor_topk(preference_text,  record_list, k):
    '''
    Get best (maximal) records according to CPTheory (MaxPref semantic)

    A record is maximal if it is satisfies a formula F and do not exist
    other record satisfied by formulas better than F
    '''

    # build theory from preference text
    theory = build_cptheory(preference_text)

    # get preference list and max formulas
    preference_list, max_formulas = theory.get_sorted_formulas()

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
