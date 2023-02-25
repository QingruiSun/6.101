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


def bacon_path(transformed_data, actor_id):
    if actor_id not in transformed_data["actor_movie"]:
        return None
    visited = set()
    visited.add(4724)
    agenda = set()
    agenda.add(4724)
    parent = {}
    while len(agenda) > 0:
        new_agenda = set()
        for actor in agenda:
            for next_actor in transformed_data["actor_actor"][actor]:
                if next_actor not in visited:
                    new_agenda.add(next_actor)
                    visited.add(next_actor)
                    parent[next_actor] = actor
        agenda = new_agenda
    path = []
    while actor_id in parent:
        path.insert(0, actor_id)
        actor_id = parent[actor_id]
    path.insert(0, 4724)
    return path


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    raise NotImplementedError("Implement me!")


def actor_path(transformed_data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == "__main__":
    with open("resources/tiny.pickle", "rb") as f:
        smalldb = pickle.load(f)
        print(smalldb)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
