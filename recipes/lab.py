"""
6.1010 Spring '23 Lab 4: Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    compound_recipes = {}
    for recipe in recipes:
        if recipe[0] == "compound":
            if recipe[1] in compound_recipes:
                compound_recipes[recipe[1]].append(recipe[2])
            else:
                compound_recipes[recipe[1]] = [recipe[2]]
    return compound_recipes


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atomic_cost = {}
    for recipe in recipes:
        if recipe[0] == "atomic":
            atomic_cost[recipe[1]] = recipe[2]
    return atomic_cost


def lowest_cost_helper(recipe_book, atomic_costs, food_item):
    if food_item in atomic_costs:
        return atomic_costs[food_item]
    recipes = recipe_book[food_item]
    min_cost = 10000000
    for recipe in recipes:
        current_cost = 0
        for element in recipe:
            current_cost += (
                lowest_cost_helper(recipe_book, atomic_costs, element[0]) * element[1]
            )
        if current_cost < min_cost:
            min_cost = current_cost
    return min_cost


def lowest_cost(recipes, food_item):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)
    return lowest_cost_helper(recipe_book, atomic_costs, food_item)


def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    raise NotImplementedError


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    raise NotImplementedError


def cheapest_flat_recipe(recipes, food_item):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    raise NotImplementedError


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes make a certain ingredient as part of a recipe, compute all
    combinations of the flat recipes.
    """
    raise NotImplementedError


def all_flat_recipes(recipes, food_item):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    raise NotImplementedError


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!
