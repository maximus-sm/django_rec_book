from factory.django import DjangoModelFactory
import factory, factory.django
from factory.faker import Faker
from movies.models import Movie, UserMoviePreferences
from functools import wraps
from random import randint
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    title = Faker("sentence", nb_words=4)
    genres = Faker(
        "pylist", nb_elements=3, variable_nb_elements=True, value_types=["str"]
    )
    # year = Faker("year")
    # year = randint(1800, 2100)
    country = Faker("country")
    # extra_data = factory.Dict({})
    extra_data = Faker("pydict", nb_elements=3, value_types=["str"])
    release_year = Faker("pyint", min_value=1800, max_value=2100)


@factory.django.mute_signals(post_save)
class UserPreferenceFactory(DjangoModelFactory):
    class Meta:
        model = UserMoviePreferences

    # We pass in profile=None to prevent UserFactory from creating another profile
    # (this disables the RelatedFactory)
    user = factory.SubFactory(
        "movies.tests.factories.UserFactory", user_preferences=None
    )
    preferences = factory.Dict({})
    watch_history = factory.List([])


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    # https://factoryboy.readthedocs.io/en/stable/recipes.html
    #
    # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call ProfileFactory(user=our_new_user), thus skipping the SubFactory.
    user_preferences = factory.RelatedFactory(
        UserPreferenceFactory, factory_related_name="user"
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
