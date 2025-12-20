from factory.django import DjangoModelFactory
from factory.faker import Faker
from movies.models import Movie
from functools import wraps
from random import randint


class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = Faker("sentence", nb_words=4)
    genres = Faker(
        "pylist", nb_elements=3, variable_nb_elements=True, value_types=["str"]
    )
    # year = Faker("year")
    # year = randint(1800, 2100)
    year = Faker("pyint", min_value=1800, max_value=2100)



# unsaved_movie = MovieFactory.build()
# saved_movie = MovieFactory.create()
# movies = MovieFactory.create_batch(5)


# def shell(a_func):

#     @wraps(a_func)
#     def wrapTheFunction():
#         print("before executing a_func()")

#         a_func()

#         print("after executing a_func()")

#     return wrapTheFunction


# def core():
#     print("I am the function which needs some decoration to remove my foul smell")

# core()

# core = shell(core)

# core()

# @shell
# def inner():
#     print("I am the function which needs some decoration to "
#           "remove my foul smell")


# print(inner)

# inner = shell(inner)

# # print(inner.__name__)

# print(inner)
