from factory.django import DjangoModelFactory
from factory.faker import Faker
from movies.models import Movie
from functools import wraps

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = Faker("sentence", nb_words=4)
    genres = Faker(
        "pylist", nb_elements=3, variable_nb_elements=True, value_types=["str"]
    )


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