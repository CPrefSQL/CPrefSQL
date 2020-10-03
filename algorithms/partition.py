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
    theory.split_rules()
    if not theory.is_consistent():
        print('inconsistent!')
        return []
    # Build formulas
    theory.build_formulas()
    # Build comparisons from formulas
    theory.build_comparisons()
    # Apply partition algorithm
    result = partition_best(theory, record_list)
    return result


def partition_best(theory, record_list):
    '''
    Get best records by partitioning the record list
    based on each comparison and separating the dominant
    records and discarding the dominated ones
    '''

    dominants = list(record_list)
    # for each comparison, verify dominant records
    for comp in theory.get_comparison_list():
        dominants, _, non_comparable = partition(dominants, comp)
        dominants = dominants + non_comparable
    return dominants


def partition(record_list, comparison):
    '''
    Uses comparison to build partitions by the record's attribute values
    and scans the the content of the partitions to separate the records
    by the comparison formulas
    '''

    # create partitions based on attributes that will be ignored
    partition_table = create_partitions(record_list, comparison)
    dominant_list = []
    non_dominants_list = []
    non_comparable_list = []

    # for each partition, separated the dominant records
    for part in partition_table:
        part_list = partition_table[part]
        part_dominant = []
        part_non_dominant = []
        part_indifferent = []
        for rec in part_list:
            if comparison.is_best_record(rec):
                part_dominant.append(rec)
            elif comparison.is_worst_record(rec):
                part_non_dominant.append(rec)
            else:
                part_indifferent.append(rec)
        if part_dominant:
            dominant_list += part_dominant
            non_dominants_list += part_non_dominant
        else:
            dominant_list += part_non_dominant

        non_comparable_list += part_indifferent

    return dominant_list, non_dominants_list, non_comparable_list


def get_partition_id(tup, attribute_set):
    '''
    Convert record attribute values into a hasheable tuple
    that can be used as a partition index
    for the hash table that represents the partitions
    '''
    att_list = []
    for att in attribute_set:
        att_list.append(tup[att])
    return tuple(att_list)


def create_partitions(tuple_list, comparison):
    '''
    Build hash table from comparison and tuples
    Tuples are grouped by "cetera paribus" atributes, so non-indifferent
    attributes must be the same
    '''
    hash_table = {}
    if len(tuple_list) > 0:
        attribute_set = set(tuple_list[0].keys())
        # ignore indifferent attributes
        attribute_set = \
            attribute_set.difference(comparison.get_indifferent_set())
        if not attribute_set:
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
    theory.split_rules()
    if not theory.is_consistent():
        return []
    # Build formulas
    theory.build_formulas()
    # Build comparisons
    theory.build_comparisons()
    # Apply algorithm
    result = partition_topk(theory, record_list, k)
    return result


def partition_topk(theory, record_list, k):
    '''
    Separate the top-k most dominant tuples
    The algorithm repeatedly scans the set of dominated tuples
    progressively populating the return list
    '''

    # initially assumes all dominant
    return_list = []
    dominant_recs = list(record_list)
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
