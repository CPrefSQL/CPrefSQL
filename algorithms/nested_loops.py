#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module with nested loop algorithms
'''
from preference.theory import build_cptheory


def get_best_and_worst(theory, record_list):
    '''
    Returns two lists: dominant list (best), dominated list (worst)
    According to CPTheory

    A record is dominant if it is not dominated by any other record
    '''
    # List of worst (dominated) records
    worst_list = []
    # List of best (dominant) records
    best_list = []
    while record_list != []:
        # Get a record
        rec = record_list.pop()
        # List of records incomparable to current record
        incomparable_list = []
        # Suppose that current record is dominant (not dominated)
        dominated = False
        # While there are record to be compared
        while record_list != []:
            # Get other record
            other_rec = record_list.pop()
            # Check if other record dominates current record
            if theory.dominates(other_rec, rec):
                # Mark current record as dominated
                dominated = True
                # Add current record into worst list
                worst_list.append(rec)
                # Add other record to incomparable list
                # It must be compared to remaining records
                incomparable_list.append(other_rec)
                break
            # Check if record dominates other record
            elif theory.dominates(rec, other_rec):
                # Add other record to dominated records
                worst_list.append(other_rec)
            # Else the records are incomparable
            else:
                incomparable_list.append(other_rec)
        record_list += incomparable_list
        # If the record was not dominated by any other
        # then it is dominant
        if not dominated:
            best_list.append(rec)
    return best_list, worst_list


def get_best(preference_text, record_list):
    '''
    Get best records according to CPTheory (classical algorithm)

    A record is best if it is not dominated by any other record
    '''
    # build theory
    theory = build_cptheory(preference_text)
    theory.split_rules()
    if not theory.is_consistent():
        return []
    result, _ = get_best_and_worst(theory, record_list)
    return result


def get_topk(preference_text, record_list, k):
    '''
    Returns the top-k records with lowest level according to a cp-theory
    '''
    # build theory
    theory = build_cptheory(preference_text)
    theory.split_rules()
    if not theory.is_consistent():
        return []
    worst_list = record_list
    topk_list = []
    while len(topk_list) < k and worst_list:
        best_list, worst_list = get_best_and_worst(theory, worst_list)
        topk_list += best_list
    if len(topk_list) > k:
        topk_list = topk_list[:k]
    return topk_list
