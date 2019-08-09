# -*- coding: utf-8 -*-
'''
Module with partition algorithms for CPref-SQL preference queries
'''

from preference.theory import build_cptheory


def get_best_partition(preference_text, record_list):
    '''
    Get best records according to CPTheory (partition algorithm)

    A record is best if it is not dominated by any other record
    '''
    theory = build_cptheory(preference_text)
    theory.build_comparisons()
    result = partition_best(theory, record_list)
    return result


def partition_best(theory, record_list):
    dominants = list(record_list)
    for comp in theory.get_comparison_list():
        dominants, _ = partition(dominants, comp)
    return dominants


def partition(record_list, comparison):
    partition_table = create_partitions(record_list, comparison)
    list_dominants = []
    list_non_dominants = []
    for part in partition_table:
        part = partition_table[part]
        part_dominant = []
        part_non_dominant = []
        part_indifferent = []
        for rec in part:
            if comparison.is_best_record(rec):
                part_dominant.append(rec)
            elif comparison.is_worst_record(rec):
                part_non_dominant.append(rec)
            else:
                part_indifferent.append(rec)
        if part_dominant:
            list_dominants = list_dominants+part
        else:
            list_dominants = list_dominants+part_dominant+part_indifferent
            list_non_dominants = list_non_dominants+part_non_dominant
    return list_dominants, list_non_dominants


def get_partition_id(tup, attribute_set):
    att_list = []
    for att in attribute_set:
        att_list.append(tup[att])
    return tuple(att_list)


def create_partitions(tuple_list, comparison):
    hash_table = {}
    attribute_set = set(tuple_list[0].keys())
    # ignore indifferent attributes
    attribute_set = attribute_set.difference(comparison.get_indifferent_set())
    if attribute_set:
        hash_table[()] = tuple_list
    else:
        for tup in tuple_list:
            # find partition id
            p_id = get_partition_id(tup, attribute_set)
            if p_id in hash_table:
                hash_table[p_id].append(tup)
            else:
                hash_table[p_id] = [tup]
    return hash_table


def get_topk_partition(preference_text, record_list, k):
    '''
    Returns the top-k records (partition algorithm)
    '''
    theory = build_cptheory(preference_text)
    theory.build_comparisons()
    result = partition_topk(theory, record_list, k)
    return result


def partition_topk(theory, record_list, k):
    dominant_recs = list(record_list)
    return_list = []

    while len(return_list) < k and dominant_recs:
        temporary_list = []
        for comp in theory.get_comparison_list():
            dominant_recs, non_dominant_recs = partition(dominant_recs, comp)
            temporary_list = temporary_list+non_dominant_recs
        return_list = return_list + dominant_recs
        dominant_recs = temporary_list
    return return_list[0:k]
