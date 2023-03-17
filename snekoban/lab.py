"""
6.1010 Spring '23 Lab 4: Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    height = len(level_description)
    width = len(level_description[0])
    player_position = ()
    grid = []
    for i in range(height):
        grid_row = []
        for j in range(width):
            if "player" in level_description[i][j]:
                player_position = (i, j)
            grid_row.append(tuple(level_description[i][j]))
        grid.append(tuple(grid_row))

    return (tuple(grid), (height, width), player_position)


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    grid = game[0]
    height = game[1][0]
    width = game[1][1]
    nr_computer = 0
    for i in range(height):
        for j in range(width):
            if "computer" in grid[i][j]:
                nr_computer += 1
            if "computer" in grid[i][j] and "target" not in grid[i][j]:
                return False
    if nr_computer == 0:
        return False
    return True


def concate_str_to_ordered_tuple(box, element):
    if len(box) == 0:
        return (element,)
    box_len = len(box)
    i = 0
    while i < box_len:
        if element < box[i]:
            break
        i += 1
    return box[0:i] + (element,) + box[i:box_len]


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    grid = game[0]
    player_position = game[2]
    height = game[1][0]
    width = game[1][1]
    new_grid = []
    for i in range(height):
        row_elements = [grid[i][j] for j in range(width)]
        new_grid.append(row_elements)
    next_actions = {"up": [-1, 0], "down": [1, 0], "left": [0, -1], "right": [0, 1]}
    next_action = next_actions[direction]
    next_player_row = player_position[0] + next_action[0]
    next_player_col = player_position[1] + next_action[1]
    if "wall" in grid[next_player_row][next_player_col]:
        return (tuple(map(tuple, new_grid)), (height, width), player_position)
    if "computer" not in grid[next_player_row][next_player_col]:
        new_grid[player_position[0]][player_position[1]] = tuple(
            [
                ele
                for ele in new_grid[player_position[0]][player_position[1]]
                if ele != "player"
            ]
        )
        new_grid[next_player_row][next_player_col] = concate_str_to_ordered_tuple(
            new_grid[next_player_row][next_player_col], "player"
        )
        return (
            tuple(map(tuple, new_grid)),
            (height, width),
            (next_player_row, next_player_col),
        )
    next_computer_row, next_computer_col = (
        next_player_row + next_action[0],
        next_player_col + next_action[1],
    )
    if (
        "computer" in grid[next_computer_row][next_computer_col]
        or "wall" in grid[next_computer_row][next_computer_col]
    ):
        return (tuple(map(tuple, new_grid)), (height, width), player_position)
    new_grid[player_position[0]][player_position[1]] = tuple(
        [
            ele
            for ele in list(new_grid[player_position[0]][player_position[1]])
            if ele != "player"
        ]
    )
    new_grid[next_player_row][next_player_col] = concate_str_to_ordered_tuple(
        new_grid[next_player_row][next_player_col], "player"
    )
    new_grid[next_player_row][next_player_col] = tuple(
        [ele for ele in new_grid[next_player_row][next_player_col] if ele != "computer"]
    )
    new_grid[next_computer_row][next_computer_col] = concate_str_to_ordered_tuple(
        new_grid[next_computer_row][next_computer_col], "computer"
    )
    return (
        tuple(map(tuple, new_grid)),
        (height, width),
        (next_player_row, next_player_col),
    )


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    height = game[1][0]
    width = game[1][1]
    grid = []
    for i in range(height):
        grid_row = []
        for j in range(width):
            grid_row.append(list(game[0][i][j]))
        grid.append(grid_row)
    return grid


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    actions = ["up", "down", "left", "right"]
    visited = set()
    agent = set()
    agent.add(game)
    visited.add(game)
    path = {}
    find = False
    victory_state = None
    nr_computer = 0
    nr_target = 0
    for i in range(game[1][0]):
        for j in range(game[1][1]):
            if "computer" in game[0][i][j]:
                nr_computer += 1
            if "target" in game[0][i][j]:
                nr_target += 1
    if nr_target < nr_computer:
        return None
    if nr_computer == 0:
        return None
    result = []
    if victory_check(game):
        return result
    while len(agent) != 0:
        print(len(agent))
        old_agent = agent
        new_agent = set()
        for state in old_agent:
            for action in actions:
                next_state = step_game(state, action)
                if next_state in visited:
                    continue
                new_agent.add(next_state)
                visited.add(next_state)
                path[next_state] = (action, state)
                if victory_check(next_state):
                    find = True
                    victory_state = next_state
                    break
            if find == True:
                break
        if find == True:
            break
        agent = new_agent
    if not find:
        return None
    state = victory_state
    reverse_actions = {"up": "down", "down": "up", "left": "right", "right": "left"}
    while state != game:
        result.insert(0, path[state][0])
        prev_state = path[state][1]
        state = prev_state
    return result


if __name__ == "__main__":
    pass
