"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    data = {}
    movie_actor = {}
    actor_movie = {}
    actor_actor = {}
    for info in raw_data:
        actor_one = info[0]
        actor_two = info[1]
        movie = info[2]
        if actor_one not in actor_movie:
            actor_movie[actor_one] = set()
        if actor_two not in actor_movie:
            actor_movie[actor_two] = set()
        actor_movie[actor_one].add(movie)
        actor_movie[actor_two].add(movie)
        if movie not in movie_actor:
            movie_actor[movie] = set()
        movie_actor[movie].add(actor_one)
        movie_actor[movie].add(actor_two)
        if actor_one not in actor_actor:
            actor_actor[actor_one] = set()
        actor_actor[actor_one].add(actor_two)
        if actor_two not in actor_actor:
            actor_actor[actor_two] = set()
        actor_actor[actor_two].add(actor_one)
    data["movie_actor"] = movie_actor
    data["actor_movie"] = actor_movie
    data["actor_actor"] = actor_actor
    return data


def acted_together(transformed_data, actor_id_1, actor_id_2):
    movie_1 = transformed_data["actor_movie"][actor_id_1]
    movie_2 = transformed_data["actor_movie"][actor_id_2]
    for movie in movie_1:
        if movie in movie_2:
            return True
    return False


def actors_with_bacon_number(transformed_data, n):
    visited = set()
    visited.add(4724)
    agenda = set()
    agenda.add(4724)
    for bacon_number in range(n):
        new_agenda = set()
        for actor in agenda:
            for next_actor in transformed_data["actor_actor"][actor]:
                if next_actor not in visited:
                    new_agenda.add(next_actor)
                    visited.add(next_actor)
        agenda = new_agenda
    return agenda


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    if (
        actor_id_1 not in transformed_data["actor_movie"]
        or actor_id_2 not in transformed_data["actor_movie"]
    ):
        return None
    visited = set()
    visited.add(actor_id_1)
    agenda = set()
    agenda.add(actor_id_1)
    parent = {}
    while len(agenda) > 0 and actor_id_2 not in visited:
        new_agenda = set()
        for actor in agenda:
            for next_actor in transformed_data["actor_actor"][actor]:
                if next_actor not in visited:
                    new_agenda.add(next_actor)
                    visited.add(next_actor)
                    parent[next_actor] = actor
        agenda = new_agenda
    path = []
    actor_id = actor_id_2
    # no path
    if actor_id not in parent:
        return None
    while actor_id in parent:
        path.insert(0, actor_id)
        actor_id = parent[actor_id]
    path.insert(0, actor_id_1)
    return path


def bacon_path(transformed_data, actor_id):
    return actor_to_actor_path(transformed_data, 4724, actor_id)


def get_movie_name(movie_id):
    with open("resources/movies.pickle", "rb") as f:
        moviedb = pickle.load(f)
        id_name = {}
        for name, ids in moviedb.items():
            if ids == movie_id:
                return name
    return None


def bacon_movie_path(transformed_data, actor_id_1, actor_id_2):
    path = actor_to_actor_path(transformed_data, actor_id_1, actor_id_2)
    if path == None:
        return None
    moviedb = None
    with open("resources/movies.pickle", "rb") as f:
        moviedb = pickle.load(f)
    movie_name_path = []
    for i in range(len(path) - 1):
        prev_actor_id = path[i]
        next_actor_id = path[i + 1]
        for prev_movie in transformed_data["actor_movie"][prev_actor_id]:
            if prev_movie in transformed_data["actor_movie"][next_actor_id]:
                movie_name_path.insert(0, get_movie_name(prev_movie))
                break
    return movie_name_path


def actor_path(transformed_data, actor_id_1, goal_test_function):
    if actor_id_1 not in transformed_data["actor_movie"]:
        return None
    path = []
    if goal_test_function(actor_id_1):
        path.append(actor_id_1)
        return path
    visited = set()
    visited.add(actor_id_1)
    agenda = set()
    agenda.add(actor_id_1)
    parent = {}
    find = False
    find_actor_id = -1
    while len(agenda) > 0 and not find:
        new_agenda = set()
        for actor in agenda:
            for next_actor in transformed_data["actor_actor"][actor]:
                if next_actor not in visited:
                    visited.add(next_actor)
                    new_agenda.add(next_actor)
                    parent[next_actor] = actor
                    if goal_test_function(next_actor):
                        find = True
                        find_actor_id = next_actor
        agenda = new_agenda
    if not find:
        return None
    actor_id = find_actor_id
    while actor_id != actor_id_1:
        path.insert(0, actor_id)
        actor_id = parent[actor_id]
    path.insert(0, actor_id_1)
    return path


def actors_connecting_films(transformed_data, film1, film2):
    if (
        film1 not in transformed_data["movie_actor"]
        and film2 not in transformed_data["movie_actor"]
    ):
        return None
    path = []
    if film1 == film2:
        return path
    visited = set()
    visited.add(film1)
    agenda = set()
    agenda.add(film1)
    find = False
    parent = {}
    parent_actor = {}
    while len(agenda) > 0:
        new_agenda = set()
        for film in agenda:
            for actor in transformed_data["movie_actor"][film]:
                for next_film in transformed_data["actor_movie"][actor]:
                    if next_film not in visited:
                        new_agenda.add(next_film)
                        visited.add(next_film)
                        parent[next_film] = film
                        parent_actor[next_film] = actor
                    if next_film == film2:
                        find = True
                        break
                if find:
                    break
            if find:
                break
        if find:
            break
        agenda = new_agenda
    if not find:
        return None
    film = film2
    while film != film1:
        path.insert(0, parent_actor[film])
        film = parent[film]
    return path


if __name__ == "__main__":
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)
        movie_name = actors_connecting_films(transform_data(smalldb), 10729, 21260)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
