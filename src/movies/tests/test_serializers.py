import pytest
from movies.models import Movie
from movies.serializers import MovieSerializer


@pytest.mark.django_db
def test_valid_movie_serializer():
    # Given valid movie data
    valid_data = {
        "title": "Inception",
        "genres": ["Action", "Sci-Fi"],
        "country": "Brasil",
        "extra_data": {},
        "release_year": 2005,
    }
    # When we create a serializer instance with this data
    serializer = MovieSerializer(data=valid_data)
    # Then, the serializer should be a valid
    assert serializer.is_valid()
    # When saving the serializer
    movie = serializer.save()
    # Then a movie instance should be created with the given data
    assert Movie.objects.count() == 1
    created_movie = Movie.objects.get()
    assert created_movie.title == valid_data["title"]
    assert created_movie.genres == valid_data["genres"]
    assert created_movie.release_year == valid_data["release_year"]
    assert created_movie.country == valid_data["country"]
    assert created_movie.extra_data == valid_data["extra_data"]


@pytest.mark.django_db
def test_invalid_movie_serializer():
    # Given invalid movie data (missing required "title" field)
    invalid_data = {"genres": ["Action", "Sci-Fi"]}
    # When we create a serializer instance with this data
    serializer = MovieSerializer(data=invalid_data)
    # Then serializer should not be valid
    assert not serializer.is_valid()
    # It should contain an error message for the missing "title" field
    assert "title" in serializer.errors


@pytest.mark.django_db
def test_serialize_movie_instance():
    # Given a movie instance
    movie = Movie.objects.create(
        title="Inception",
        genres=["Action", "Sci-Fi"],
        release_year=2010,
        country="Columbia",
    )
    # When we serialize the movie
    serializer = MovieSerializer(movie)
    # Then the resulting JSON data should contain the movie's details
    assert serializer.data == {
        "id": movie.id,
        "title": movie.title,
        "genres": movie.genres,
        "release_year": movie.release_year,
        "extra_data": movie.extra_data,
        "country": movie.country,
    }
