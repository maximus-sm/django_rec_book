import pytest
import json
from .factories import MovieFactory, UserFactory, UserPreferenceFactory
from movies.models import UserMoviePreferences, Movie
from movies.services import add_preference, add_watch_history
from django.contrib.auth import get_user_model
from django.http import Http404
@pytest.mark.django_db
def test_add_preference_succes():
    data = {"body": "big tits", "actor": "Rosumund Pike", "dorama": "yessss"}
    user = UserPreferenceFactory()
    print(vars(user))
    assert user.preferences == {}
    print(user.preferences)
    add_preference(user.user.id, data)
    # user = get_user_model().objects.filter(movie_preferences__id=user.id)
    user = UserMoviePreferences.objects.filter(id=user.id).first()
    assert user.preferences["actor"] == [data["actor"]]


@pytest.mark.django_db
def test_add_same_preference_twice():
    data = {"body": "big tits", "actor": "Rosumund Pike", "dorama": "yessss"}
    user = UserPreferenceFactory()
    print(vars(user))
    assert user.preferences == {}
    print(user.preferences)
    add_preference(user.user.id, data)
    add_preference(user.user.id, {"actor": "Rosumund Pike"})
    # user = get_user_model().objects.filter(movie_preferences__id=user.id)
    user = UserMoviePreferences.objects.filter(id=user.id).first()
    # ensure same value not added again.
    assert user.preferences["actor"] == [data["actor"]]


@pytest.mark.django_db
def test_add_watch_history():
    movie = MovieFactory()
    user = UserFactory()
    data = {
        "title": movie.title,
        "year": movie.release_year,
        "director": movie.extra_data.get("directors", []),
        "genre":movie.genres,
    }
    add_watch_history(user.id, movie.id)
    watch_history = UserMoviePreferences.objects.filter(user_id=user.id).first().watch_history[0]
    assert watch_history == data
    
    
@pytest.mark.django_db
@pytest.mark.xfail(raises=Http404)
def test_add_watch_history_non_existing_movie():
    # movie = MovieFactory()
    user = UserFactory()
    # data = {
    #     "title": movie.title,
    #     "year": movie.release_year,
    #     "director": movie.extra_data.get("directors", []),
    #     "genre":movie.genres,
    # }
    # info = False
    add_watch_history(user.id, 2)

    # with pytest.raises(Http404) as exception:
    #     # info = True
    #     raise Exception("Che tam")
    
    # assert exception.value == "Che tam"
    
    
    # watch_history = UserMoviePreferences.objects.filter(user_id=user.id).first().watch_history[0]
    # assert watch_history == data