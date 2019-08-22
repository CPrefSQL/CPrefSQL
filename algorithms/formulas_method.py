#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module with new algorithms
'''

import copy

from preference.theory import build_cptheory
from preference.comparison import _is_record_valid_by_formula
from preference.btg_graph import BTG_Graph


def get_formulas_best(preference_text, record_list):
    '''
    Get best records according to CPTheory (formulas algorithm)

    A record is best if it is not dominated by any other record
    '''

    theory = build_cptheory(preference_text)
    theory.build_formulas()

    max_formulas = get_max_formulas(theory._formula_list)
    theory._formula_list = max_formulas
    theory.build_comparisons()

    graph = BTG_Graph()
    translate_table = {}

    # build BTG graph with the formulas
    for cp in theory._comparison_list:
        key1 = str(cp._best_formula_dict)
        key2 = str(cp._worst_formula_dict)

        if key1 not in translate_table:
            translate_table[key1] = cp._best_formula_dict

        if key2 not in translate_table:
            translate_table[key2] = cp._worst_formula_dict

        graph.add_edge(key1, key2)

    # return the topological ordering of the graph
    preference_list = graph_to_preference_list(graph)

    # search for the records with the lowest level
    t = []
    best_level = float("Inf")

    for rec in record_list:

        for level_list, formula_list in enumerate(preference_list):
            for formula in formula_list:
                # if find lower level, discard old records and reset best level
                if _is_record_valid_by_formula(translate_table[formula], rec):

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


def get_max_formulas(formula_list):
    '''
    Extract the max formulas from the lists
    '''

    formula_length = 0
    for formula in formula_list:
        if len(formula) > formula_length:
            formula_length = len(formula)

    max_formulas = []
    for formula in formula_list:
        if len(formula) == formula_length:
            max_formulas.append(formula)

    return max_formulas


def remove_non_related_formulas(formula_list, comparison_list):
    related_formulas = []
    for fm in formula_list:
        for cp in comparison_list:
            if cp.is_best_formula(fm) or cp.is_worst_formula(fm):
                related_formulas.append(fm)
                break

    return related_formulas


def graph_to_preference_list(btg_graph):

    # make a copy of the graph
    graph = copy.deepcopy(btg_graph)

    preference_list = []
    top_nodes = graph.get_top_vertex()

    while len(top_nodes) > 0:
        preference_list.append(top_nodes)

        # remove edges from graph
        for node in top_nodes:
            graph._graph_dict.pop(node)

        # get next level of nodes
        top_nodes = graph.get_top_vertex()

    return preference_list


def get_formulas_topk(preference_text,  record_list, k):
    '''
    Get k best records according to CPTheory (formulas algorithm)

    A record is best if it is not dominated by any other record
    '''

    theory = build_cptheory(preference_text)
    theory.build_formulas()

    max_formulas = get_max_formulas(theory._formula_list)
    theory._formula_list = max_formulas
    theory.build_comparisons()

    graph = BTG_Graph()
    translate_table = {}

    # build BTG graph with the formulas
    for cp in theory._comparison_list:
        key1 = str(cp. _best_formula_dict)
        key2 = str(cp. _worst_formula_dict)

        if key1 not in translate_table:
            translate_table[key1] = cp._best_formula_dict

        if key2 not in translate_table:
            translate_table[key2] = cp._worst_formula_dict

        graph.add_edge(key1, key2)

    # return the topological ordering of the graph
    preference_list = graph_to_preference_list(graph)

    # search for the records with the lowest level
    t = []

    for formula_list in preference_list:
        for formula in formula_list:

            for rec in record_list:
                # if find lower level, discard old records and reset best level
                if _is_record_valid_by_formula(translate_table[formula], rec):
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
