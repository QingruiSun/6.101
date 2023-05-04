"""
6.1010 Spring '23 Lab 8: SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing
import doctest

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def assignment_variable(formula, variable, value):
    new_formula = []
    possible_formula = True

    for clause in formula:
        new_clause = []
        select_clause = True
        variable_literal = None
        for literal in clause:
            if literal[0] == variable:
                if literal[1] == value:
                    select_clause = False
                    break
                else:
                    variable_literal = literal
                    
            else:
                new_clause.append(literal)
        if len(new_clause) == 0 and variable_literal != None:
            possible_formula = False
            new_clause.append(variable_literal)
        if select_clause:
            new_formula.append(new_clause)
    
    return new_formula, possible_formula

def parse_variable_list(formula):
    variable_set = set()
    for clause in formula:
        for literal in clause:
            variable_set.add(literal[0])
    return list(variable_set)


def satisfying_assignment_helper(formula, variable_list, index, result_map):
    if index >= len(variable_list):
        return True
    true_formula, true_formula_possible = assignment_variable(formula, variable_list[index], True)
    if true_formula_possible:
        true_formula_possible = satisfying_assignment_helper(true_formula, variable_list, index + 1, result_map)
    if true_formula_possible:
        result_map[variable_list[index]] = True
        return True
    false_formula, false_formula_possible = assignment_variable(formula, variable_list[index], False)
    if false_formula_possible:
        false_formula_possible = satisfying_assignment_helper(false_formula, variable_list, index + 1, result_map)
    if false_formula_possible:
        result_map[variable_list[index]] = False
        return True

    return False


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    result_map = {}
    variable_list = parse_variable_list(formula)
    possible = satisfying_assignment_helper(formula, variable_list, 0, result_map)
    if possible:
        return result_map
    return None


def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    raise NotImplementedError


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    raise NotImplementedError


if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
