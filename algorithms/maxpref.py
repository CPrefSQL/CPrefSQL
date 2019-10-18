#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module with new algorithms
'''

from preference.theory import build_cptheory
from preference.comparison import _is_record_valid_by_formula
import copy


def get_maxpref_best(preference_text, record_list):
    '''
    Get best (maximal) records according to CPTheory (MaxPref semantic)

    A record is maximal if it is satisfies a formula F and there is
    no other record that satisfies a formula better than F
    '''

    # Build theory from preference text
    theory = build_cptheory(preference_text)

    # Get maximal formulas and sorted formula list
    sorted_list = theory.get_sorted_formulas()
    max_formulas = theory.get_max_formulas()

    # List of records to be returned
    result_list = []
    # Current formula level (anyone is smaller then plus infinity)
    current_level = float("Inf")

    # copy record lists because algorithm needs to modify the list
    records = copy.deepcopy(record_list)

    # For each input record
    for rec in records:
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
        return records
    return result_list


def get_maxpref_topk(preference_text,  record_list, k):
    '''
    Get top-k (maximal) records according to CPTheory (MaxPref semantic)
    '''
    # Build theory from preference text
    theory = build_cptheory(preference_text)
    # Get maximal formulas and sorted formula list
    sorted_list = theory.get_sorted_formulas()
    max_formulas = theory.get_max_formulas()
    # List of records to be returned
    result_list = []

    # copy record lists because algorithm needs to modify it
    records = copy.deepcopy(record_list)

    # TODO: scanning formula the list might be faster,
    # because no sorting is required
    # For each input record
    for rec in records:
        # For each sub_list of sorted formulas
        for formula_level, formula_list in enumerate(sorted_list):
            # For each formula in current formula level
            for formula_id in formula_list:
                # If record is satisfied by current formula
                if _is_record_valid_by_formula(max_formulas[formula_id], rec):
                    # Label the record with formula level
                    rec_level = (formula_level, rec)
                    # Append to result list
                    result_list.append(rec_level)
    # Sort records according to formula level
    result_list.sort()
    # Remove formula level
    result_list = [tup[1] for tup in result_list]
    return result_list[:k]
