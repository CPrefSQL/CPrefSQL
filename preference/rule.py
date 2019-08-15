# -*- coding: utf-8 -*-
'''
Module to manipulate conditional preference rules (cp-rules)
'''

from grammar.symbols import IF_SYM, THEN_SYM
from preference.interval import get_str_predicate, intersect


# TODO: Join in a single class
class CPCondition(object):
    '''
    Class to represent rule condition
    '''
    def __init__(self, parsed_condition):
        # Rule condition dictionaries
        self._condition_dict = {}
        if parsed_condition is not None:
            for parsed_pred in parsed_condition:
                # Get attribute
                att = parsed_pred.get_attribute()
                # Get interval
                self._condition_dict[att] = parsed_pred.get_interval()

    def __str__(self):
        str_list = [get_str_predicate(att, self._condition_dict[att])
                    for att in self._condition_dict]
        return ' AND '.join(str_list)

    def __len__(self):
        return len(self._condition_dict)

    def copy(self):
        '''
        Create a copy
        '''
        copy_cond = CPCondition(None)
        copy_cond.__dict__.update(self.__dict__)
        return copy_cond

    def get_condition_dict(self):
        '''
        Get condition dictionary
        '''
        return self._condition_dict

    def get_attribute_list(self):
        '''
        Get all attributes present in the condition
        '''
        return self._condition_dict.keys()

    def is_compatible(self, other):
        '''
        Check if a condition is compatible with another condition.
        A condition is compatible with another condition if
        their interval overlaps for the same attributes
        '''
        other_cond_dict = other.get_condition_dict()
        for key in self._condition_dict:
            if key in other_cond_dict \
                    and not intersect(self._condition_dict[key],
                                      other_cond_dict[key]):
                return False
        return True

    def is_satisfied_by(self, record):
        '''
        Check if conditions is satisfied by a record
        '''
        return is_dict_satisfied_by(self._condition_dict, record)

    def get_atomic_formulas_list(self):
        '''
        Get atomic formulas for present conditions
        '''
        formulas_list = []
        # Get intervals in antecedent
        for att in self._condition_dict:
            formula = {att: self._condition_dict[att]}
            formulas_list.append(formula)
        return formulas_list


class CPPreference(object):
    '''
    Class to represent rule preference
    '''
    def __init__(self, parsed_best, parsed_worst, indifferent_list):
        '''
        Initialize rule by a ParsedRule
        '''
        # Preference attribute
        self._attribute = None
        # Preferred Interval
        self._best_interval = None
        # non preferred interval
        self._worst_interval = None
        # Indifferent attributes
        self._indifferent_attribute_set = set()
        if parsed_best is not None and parsed_worst is not None and \
                indifferent_list is not None:
            self._attribute = parsed_best.get_attribute()
            # Get preferred and non preferred intervals
            self._best_interval = parsed_best.get_interval()
            self._worst_interval = parsed_worst.get_interval()
            self._indifferent_attribute_set = set(indifferent_list)

    def __str__(self):
        pref_str = get_str_predicate(self._attribute, self._best_interval)
        pref_str += ' BETTER THAN ' + \
            get_str_predicate(self._attribute, self._worst_interval)
        indiff_str_list = [str(att) for att in self._indifferent_attribute_set]
        pref_str += '[' + ', '.join(indiff_str_list) + ']'
        return pref_str

    def get_preference_attribute(self):
        '''
        Get preference attribute
        '''
        return self._attribute

    def get_best_interval(self):
        '''
        Get preferred value for preference attribute
        '''
        return self._best_interval

    def get_worst_interval(self):
        '''
        Get non preferred value for preference attribute
        '''
        return self._worst_interval

    def get_indifferent_set(self):
        '''
        Get indifferent attribute set
        '''
        return self._indifferent_attribute_set

    def is_best_satisfied_by(self, record):
        '''
        Check if a record satisfies the best interval
        '''
        return self._attribute in record and \
            intersect(self._best_interval, record[self._attribute])

    def is_worst_satisfied_by(self, record):
        '''
        Check if a record satisfies the worst interval
        '''
        return self._attribute in record and \
            intersect(self._worst_interval, record[self._attribute])

    def copy(self):
        '''
        Create a copy
        '''
        copy_pref = CPPreference(None, None, None)
        copy_pref.__dict__.update(self.__dict__)
        return copy_pref


class CPRule(object):
    '''
    Class to represent a conditional preference rule
    '''

    def __init__(self, parsed_rule):
        # Rule condition
        self._condition = None
        # Rule Preference
        self._preference = None
        # Initialize rule condition
        if parsed_rule.condition:
            self._condition = CPCondition(parsed_rule.condition)
        # Initialize rule preference
        self._preference = CPPreference(parsed_rule.best,
                                        parsed_rule.worst,
                                        parsed_rule.indifferent)

    def __str__(self):
        rule_str = ''
        if self._condition:
            rule_str = IF_SYM + ' ' + str(self._condition) + ' ' + \
                THEN_SYM + ' '
        rule_str += str(self._preference)
        return rule_str

    def __repr__(self):
        return self.__str__()

    # Used for set of rules
    def __cmp__(self, other):
        if type(self) != type(other):  # IGNORE:unidiomatic-typecheck
            return 1
        return cmp(str(self), str(other))

    # Used for set of rules
    def __eq__(self, other):
        return isinstance(other, CPRule) and str(self) == str(other)

    # Used for set of rules
    def __ne__(self, other):
        return not self.__eq__(other)

    # Used for set of rules
    def __hash__(self):
        return hash(str(self))

    def get_condition(self):
        '''
        Get rule condition
        '''
        return self._condition

    def get_preference(self):
        '''
        Get rule preference
        '''
        return self._preference

    def copy(self):
        '''
        Create a copy
        '''
        copy_rule = CPRule(None)
        copy_rule.__dict__.update(self.__dict__)
        return copy_rule

    def change_record(self, record):
        '''
        Generate a worst record when it is possible,
        when it is not then return None
        '''
        cond = self._condition
        pref = self._preference
        pref_att = pref.get_preference_attribute()
        best_interval = pref.get_best_interval()
        if cond is None or cond.is_satisfied_by(record):
            if pref_att in record and \
                    intersect(best_interval, record[pref_att]):
                new_record = record.copy()
                new_record[pref_att] = pref.get_worst_interval()
                for att in pref.get_indifferent_set():
                    if att in new_record:
                        del new_record[att]
                return new_record
        return None

    def get_atomic_formulas_list(self):
        '''
        Get atomic formulas in rule
        '''
        formulas_list = []
        if self._condition:
            formulas_list += self._condition.get_atomic_formulas_list()
        formula = {self._preference.get_preference_attribute():
                   self._preference.get_best_interval()}
        formulas_list.append(formula)
        formula = {self._preference.get_preference_attribute():
                   self._preference.get_worst_interval()}
        formulas_list.append(formula)
        return formulas_list

    def get_attribute_list(self):
        '''
        Get attribute list present in rule
        '''
        cond = self._condition
        pref = self._preference
        att_list = cond.get_attribute_list() + list(pref.get_indifferent_set())
        att_list.append(pref.get_preference_attribute())
        return att_list

    def is_compatible_to(self, other):
        '''
        Check if a rule is compatible with another rule

        A rule is compatible with another rule
        if they are over the same preference attribute
        and they have the same value to same attributes
        in the present conditions
        '''
        if self.get_preference().get_preference_attribute() != \
                other.get_preference().get_preference_attribute():
            return False
        elif self._condition is not None \
                and other.get_condition() is not None \
                and not self._condition.is_compatible(other.get_condition()):
            return False
        return True

    def dominates(self, record1, record2):
        '''
        Returns True if record1 dominates (is preferred to) record2
        according to rule
        '''
        # Check if record1 has preferred value
        # and other formula1 has non preferred value
        pref = self._preference
        if not pref.is_best_satisfied_by(record1) or \
                not pref.is_worst_satisfied_by(record2):
            return False
        # Check if formulas satisfy rule conditions
        cond = self._condition
        if cond:
            if not cond.is_satisfied_by(record1) or \
                    not cond.is_satisfied_by(record2):
                return False
        # Check if all another attributes are equal except
        # Preference attribute and indifferent attributes
        att_set = set(record1.keys() + record2.keys())
        att_set = att_set.difference(set([pref.get_preference_attribute()]))
        att_set = att_set.difference(pref.get_indifferent_set())
        for att in att_set:
            if att not in record1 or \
                    att not in record2 or \
                    record1[att] != record2[att]:
                return False
        return True


def is_dict_satisfied_by(condition_dict, record):
    '''
    Check if a record satisfies a condition dictionary
    '''
    for att in condition_dict:
        interval = condition_dict[att]
        if att not in record or \
                not intersect(interval, record[att]):
            return False
    return True
