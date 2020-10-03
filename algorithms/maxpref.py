# -*- coding: utf-8 -*-
'''
Module with extended partition algorithms for Maxpref CPref-SQL operators
'''

from preference.theory import build_cptheory
from partition import partition


def incomparable(comparisons, record_list):
    non_comparables = record_list
    comparables = []
    for comp in comparisons:
        dominants, non_dominants, non_comparables = \
            partition(non_comparables, comp)
        comparables += dominants + non_dominants
    return comparables, non_comparables


def get_mbest_partition(preference_text, record_list):
    '''
    Get best records according to CPTheory (partition algorithm)
    A record is best if it is not dominated by any other record
    '''
    theory = build_cptheory(preference_text)
    theory.split_rules()
    if not theory.is_consistent():
        return []
    # Build formulas
    theory.build_formulas()
    # Build comparisons from formulas
    theory.build_comparisons()
    # Apply partition algorithm
    result = partition_mbest(theory, record_list)
    return result


def partition_mbest(theory, record_list):
    '''
    Get best records by partitioning the record list
    based on each comparison and separating the dominant
    records and discarding the dominated ones
    '''

    dominants = list(record_list)
    dominants, _ = incomparable(theory.get_comparison_list(), dominants)

    # for each comparison, verify dominant records
    for comp in theory.get_comparison_list():
        dominants, _, non_comparables = partition(dominants, comp)
        dominants = dominants + non_comparables
    return dominants


def get_mtopk_partition(preference_text, record_list, k):
    '''
    Returns the top-k records (partition algorithm)
    '''
    theory = build_cptheory(preference_text)
    theory.split_rules()
    if not theory.is_consistent():
        return []
    # Build formulas
    theory.build_formulas()
    # Build comparisons
    theory.build_comparisons()
    # Apply algorithm
    result = partition_mtopk(theory, record_list, k)
    return result


def partition_mtopk(theory, record_list, k):
    '''
    Separate the top-k most dominant tuples
    The algorithm repeatedly scans the set of dominated tuples
    progressively populating the return list
    '''
    # initially assumes all dominant
    return_list = []
    dominant_recs = list(record_list)
    dominant_recs, _ = \
        incomparable(theory.get_comparison_list(), dominant_recs)

    while len(return_list) < k and dominant_recs:
        temporary_list = []
        # for each comparison, verify dominant records
        for comp in theory.get_comparison_list():
            dominant_recs, non_dominant_recs, non_comparable = \
                partition(dominant_recs, comp)
            temporary_list = temporary_list + non_dominant_recs
            dominant_recs = dominant_recs + non_comparable
        return_list = return_list + dominant_recs
        dominant_recs = temporary_list
    return return_list[0:k]
