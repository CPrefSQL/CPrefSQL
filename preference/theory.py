#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module to manipulate conditional preference theories (cp-theories)
'''

from preference.graph import PreferenceGraph
from preference.comparison import build_comparison, Comparison
from preference.interval import intersect
from grammar.theory_grammar import TheoryGrammar
from preference.rule import CPRule


class CPTheory(object):
    '''
    Class to represent a conditional preference theory
    '''
    def __init__(self, rule_list):
        # List of rules
        self._rule_list = rule_list
        # List of formulas (used by partition method)
        self._formula_list = []
        # List of comparisons (used by partition method)
        self._comparison_list = []

    def __len__(self):
        return len(self._rule_list)

    def __str__(self):
        rule_str_list = [str(rule) for rule in self._rule_list]
        return '\n'.join(rule_str_list)

    def __repr__(self):
        return self.__str__()

    def is_consistency(self):
        '''
        Check theory consistency
        '''
        if self._is_global_consistent() \
                and self._is_local_consistent():
            return True
        return False

    def _is_global_consistent(self):
        '''
        Check global consistency of theory

        Build a graph with edges (C) -> (P) and (P) -> (I), where:
            (C) are the attributes in the condition
            (P) is the rule attribute
            (I) are the rule indifferent attributes
        All rules are considered
        If builded graph is acyclic, then theory is globally consistent
        '''
        # Initialize graph
        graph = PreferenceGraph()
        # For each rule
        for rule in self._rule_list:
            # For each condition in rule
            cond = rule.get_condition()
            pref = rule.get_preference()
            if cond is not None:
                for att in cond.get_condition_dict():
                    # Add edge (C) -> (P)
                    graph.add_edge(att, pref.get_preference_attribute())
            # For each indifferent attribute
            for indiff_att in pref.get_indifferent_set():
                # Add edge (P) -> (I)
                graph.add_edge(pref.get_preference_attribute(), indiff_att)
        # Check if graph is acyclic
        return graph.is_acyclic()

    def _get_rule_list_by_attribute(self, attribute):
        '''
        Get rules with attribute key is equal specified attribute
        '''
        rules_list = []
        for rule in self._rule_list:
            if rule.get_preference_attribute() == attribute:
                rules_list.append(rule)
        return rules_list

    def _is_local_consistent(self):
        '''
        Check if theory is local consistent

        A theory is local inconsistent if there are a set of compatible rules
        such that an interval is preferred than itself
        '''
        for rule_set in self._get_compatible_sets():
            rule_list = [self._rule_list[index] for index in rule_set]
            graph = _build_interval_graph(rule_list)
            if not graph.is_acyclic():
                return False
        return True

    def _build_formulas(self):
        '''
        Generate a list of formulas combining all intervals of attributes
        '''
        # Get atomic formulas in all rules
        atomic_formula_list = []
        for rule in self._rule_list:
            for formula in rule.get_atomic_formulas_list():
                if formula not in self._formula_list:
                    self._formula_list.append(formula)
                    atomic_formula_list.append(formula)
        # Combined formulas
        for atomic in atomic_formula_list:
            new_formula_list = []
            att = atomic.keys()[0]
            for formula in self._formula_list:
                if att not in formula:
                    formula_copy = formula.copy()
                    formula_copy[att] = atomic[att]
                    if formula_copy not in self._formula_list \
                            and formula_copy not in new_formula_list:
                        new_formula_list.append(formula_copy)
            self._formula_list += new_formula_list

    def _clean_comparisons(self):
        '''
        Remove not essential comparisons
        '''
        # Copy comparison list
        initial_list = self._comparison_list[:]
        # List of essential comparisons
        essential_list = []
        # Run while there is comparisons to process
        while initial_list:
            # Take one comparison
            comp = initial_list.pop()
            # Suppose comparison is essential
            essential = True
            # Check all another comparisons
            for other_comp in initial_list + essential_list:
                # Check if other comparison is more generic
                if other_comp.is_more_generic_than(comp):
                    # So, comparison is not essential
                    essential = False
                    break
            # If no one is more generic, comparison is essential
            if essential:
                essential_list.append(comp)
        self._comparison_list = essential_list

    def build_comparisons(self):
        '''
        Generate comparisons
        '''
        # Build formulas
        self._build_formulas()
        # Generate direct comparisons
        comp_dict = {}
        for idx1, formula1 in enumerate(self._formula_list):
            comp_dict[idx1] = {}
            for idx2, formula2 in enumerate(self._formula_list):
                tmp_set = set()
                if idx1 != idx2:
                    for rule in self._rule_list:
                        # Check if formula1 dominates formula2
                        if rule.formula_dominates(formula1, formula2):
                            comp = build_comparison(formula1, formula2, rule)
                            tmp_set.add(comp)
                comp_dict[idx1][idx2] = tmp_set
        self._build_transitive_comparisons(comp_dict)

    def _build_transitive_comparisons(self, comp_dict):
        '''
        Generate transitive comparisons (Floyd-Warshall Algorithm)
        '''
        # Generate transitive
        for k in range(len(self._formula_list)):
            for i in range(len(self._formula_list)):
                for j in range(len(self._formula_list)):
                    ik_set = comp_dict[i][k]
                    kj_set = comp_dict[k][j]
                    if ik_set and kj_set:
                        comp_set = _combine_transitive(ik_set, kj_set)
                        comp_set = comp_set.union(comp_dict[i][j])
                        comp_dict[i][j] = comp_set
        self._comparison_list = []
        for i in range(len(self._formula_list)):
            for j in range(len(self._formula_list)):
                self._comparison_list += list(comp_dict[i][j])
        # Remove non essential comparisons
        self._clean_comparisons()
        self._comparison_list.sort()

    def dominates(self, record1, record2):
        '''
        Returns True if record1 dominates (is preferred to) record2
        according to theory (dominance test by search)
        '''
        if record1 != record2:
            return _dominates_by_search(self._rule_list, record1, record2)
        return False

    def _get_compatible_sets(self):
        '''
        Get a list of maximal sets of compatible rules

        Two CPRules are compatibles if they have the same preference attribute
        and their conditions are compatibles
        '''
        # Initial list of sets (one rule per set)
        set_list = [set([rule_id]) for rule_id in range(len(self._rule_list))]
        change = True
        # Suppose no changes
        while change:
            change = False
            # New list of combined sets
            new_set_list = []
            for rule_set in set_list:
                # Suppose no combination
                combined = False
                # For each rules
                for rule_id in range(len(self._rule_list)):
                    # Check if rule is compatible with set
                    # and rule not in this set
                    if self._is_cprule_compatible_to_list(rule_id, rule_set) \
                            and rule_id not in rule_set:
                        combined = True
                        # Create new set and add this rule
                        new_set = rule_set.copy()
                        new_set.add(rule_id)
                        # Check if set does not exists
                        if new_set not in new_set_list:
                            change = True
                            new_set_list.append(new_set)
                # if there was not combinations consider original set
                if not combined:
                    new_set_list.append(rule_set)
            set_list = new_set_list
        return set_list

    def _is_cprule_compatible_to_list(self, rule_id, rule_id_list):
        '''
        Check if a cp-rule is compatible to every other cp-rule in a list
        '''
        cprule = self._rule_list[rule_id]
        for other_id in rule_id_list:
            other = self._rule_list[other_id]
            if not cprule.is_compatible_to(other):
                return False
        return True

    def get_comparison_list(self):
        '''
        Return the comparison list
        '''
        return self._comparison_list

    def get_btg(self, record_list):
        '''
        Debug a BTG over a record list according to rules of theory
        '''
        str_btg = "\nTuples:"
        for index, record in enumerate(record_list):
            str_btg += "\nt" + str(index + 1) + " = " + str(record)
        str_btg += "\n\nRules:"
        for index, rule in enumerate(self._rule_list):
            str_btg += "\n(R" + str(index + 1) + ") = " + str(rule)
        str_btg += "\n\nDirect BTG:"
        for index1, record1 in enumerate(record_list):
            for index2, record2 in enumerate(record_list):
                for index, rule in enumerate(self._rule_list):
                    if rule.record_dominates(record1, record2):
                        str_btg += "\nt" + str(index1+1) + \
                            " (R" + str(index+1) + ") t" + str(index2+1)
        str_btg += "\n\nFull BTG:"
        for index1, record1 in enumerate(record_list):
            for index2, record2 in enumerate(record_list):
                if self.dominates(record1, record2):
                    str_btg += "\nt" + str(index1 + 1) + \
                            " -> t" + str(index2 + 1)
        return str_btg


def _build_interval_graph(rule_list):
    '''
    Build a graph with edges (P) -> (NP) over a rule list

    (P) is the preferred interval and (NP) is the non preferred interval
    of each rule
    '''
    graph = PreferenceGraph()
    for rule in rule_list:
        pref = rule.get_preference()
        graph.add_edge(pref.get_best_interval(),
                       pref.get_worst_interval())
    return graph


def is_goal_record(curren_record, goal_record):
    '''
    Check if first record reaches goal record

    A record reaches a goal if its attributes are inside or equal of
    correspondent goal attributes
    Indifferent attributes of goal are ignored
    '''
    for att in curren_record:
        if att not in goal_record \
                or intersect(goal_record[att], curren_record[att]):
            continue
        else:
            return False
    return True


def _combine_transitive(set1, set2):
    '''
    Combine two set of transitive comparisons
    b: f1 > f2[W] and b': f1' > f2'[W'] are transitive if
    f2 = f1'
    The combination of then is b'': f1 > f2' [W + W']
    '''
    result_set = set()
    for comp1 in set1:
        for comp2 in set2:
            indiff_set = comp1.get_indifferent_set()
            indiff_set = indiff_set.union(comp2.get_indifferent_set())
            comp = Comparison(comp1.get_preferred_formula(),
                              comp2.get_notpreferred_formula(),
                              indiff_set)
            result_set.add(comp)
    return result_set


def _dominates_by_search(rule_list, record1, record2):
    '''
    Returns True if record1 dominates (is preferred to) record2
    according to theory (dominance test by search)
    '''
    # Check if record2 is the goal (record1)
    if is_goal_record(record1, record2):
        return True
    # For every rule
    for index, rule in enumerate(rule_list):
        # try to create new record by applying current rule
        new_rec = rule.change_record(record1)
        # Check if new record is valid
        if new_rec is not None:
            # Create new rule list excluding current rule
            new_rule_list = [rule2
                             for index2, rule2 in enumerate(rule_list)
                             if index != index2]
            # Make the recursive call
            if _dominates_by_search(new_rule_list, new_rec, record2):
                return True
    return False


def build_cptheory(preference_text):
    '''
    Build a cp-theory from a text
    '''
    parsed = TheoryGrammar.parse(preference_text)
    if parsed is not None:
        rule_list = []
        for parsed_rule in parsed:
            cp_rule = CPRule(parsed_rule)
            rule_list.append(cp_rule)
    return CPTheory(rule_list)
