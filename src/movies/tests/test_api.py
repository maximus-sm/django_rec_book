import pytest
import json
from .factories import MovieFactory, UserFactory
from django.urls import reverse, resolve
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient
from movies.models import Movie
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile


# @pytest.mark.django_db
# def test_create_movie(client):
#     url = reverse("movies:movie-list")
#     data = json.dumps(
#         {
#             "title": "A New Hope",
#             "genres": ["Sci-Fi", "Drama"],
#             "country": "Germany",
#             "release_year": 2004,
#             "extra_data": {},
#         }
#     )
#     # print(data)
#     response = client.post(path=url, data=data, content_type="application/json")
#     # wrong attribute json.Why?
#     # response = client.post(path=url, json=data)
#     # print(response.json) # no respone.json()
#     assert response.status_code == status.HTTP_201_CREATED, response.json()
#     assert Movie.objects.filter(title="A New Hope").count() == 1


# @pytest.mark.django_db
# def test_retrieve_movie(client):
#     movie = MovieFactory()
#     url = reverse("movies:movie-detail", kwargs={"pk": movie.id})
#     # print(resolve("movies"))
#     response = client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {
#         "id": movie.id,
#         "title": movie.title,
#         "genres": movie.genres,
#         "country": movie.country,
#         "release_year": movie.release_year,
#         "extra_data": movie.extra_data,
#     }


# @pytest.mark.django_db
# def test_update_movie(client):
#     movie = MovieFactory()
#     print(movie.country)
#     new_title = "Updated Movie Title"
#     new_country = "Angola"
#     url = reverse("movies:movie-detail", kwargs={"pk": movie.id})
#     data = {"title": new_title, "country": new_country}
#     response = client.patch(url, data=data, content_type="application/json")
#     print(movie.country)
#     assert response.status_code == status.HTTP_200_OK, response.json()
#     movie = Movie.objects.filter(id=movie.id).first()
#     assert movie
#     assert movie.title == new_title
#     assert movie.country == new_country


# @pytest.mark.django_db
# def test_delete_movie(client):
#     movie = MovieFactory()
#     url = reverse("movies:movie-detail", kwargs={"pk": movie.id})
#     response = client.delete(url)
#     assert response.status_code == status.HTTP_204_NO_CONTENT
#     assert not Movie.objects.filter(id=movie.id).exists()


# @pytest.mark.django_db
# @override_settings(REST_FRAMEWORK={"PAGE_SIZE": 10})  # Override the PAGE_SIZE setting
# def test_list_movies_with_pagination(client):
#     # Create a batch of movies, adjust the number according to your PAGE_SIZE setting
#     movies = MovieFactory.create_batch(10)
#     # Define the URL for the list movies endpoint
#     url = reverse("movies:movie-list")
#     # Perform a GET request to the list endpoint
#     response = client.get(url)
#     # Assert that the response status code is 200 OK
#     assert response.status_code == status.HTTP_200_OK
#     # Convert the response data to JSON
#     data = response.json()
#     # Assert the structure of the paginated response
#     assert "count" in data
#     assert "next" in data
#     assert "previous" in data
#     assert "results" in data
#     # Assert that the count matches the total number of movies created
#     assert data["count"] == 10
#     # Adjust according to the number of movies created
#     # Assert the pagination metadata (if applicable,
#     # depending on the number of items and page size)
#     # For example, if you expect more items and multiple pages:
#     # assert data["next"] is not None
#     # But in this case, if all movies fit on one page:
#     assert data["next"] is None
#     assert data["previous"] is None


# mark.parametrize calls the dedicated funtion with given parametres and data.
# if the data is the list, the function called the number of list elemnt times?
@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_preferences, expected_genre",
    [
        ({"genre": "sci-fi"}, "sci-fi"),
        ({"genre": "drama"}, "drama"),
        ({"genre": "action"}, "action"),
        ({"genre": "sci-fi", "actor": "Sigourney Weaver", "year": "1979"}, "sci-fi"),
    ],
)
def test_add_and_retrieve_preferences_success(new_preferences, expected_genre):
    user = UserFactory()
    client = APIClient()
    preferences_url = reverse("movies:user-preferences", kwargs={"user_id": user.id})
    # Add new preferences
    response = client.post(
        preferences_url, {"new_preferences": new_preferences}, format="json"
    )
    assert response.status_code in [200, 201]
    # Retrieve preferences to verify
    response = client.get(preferences_url)
    assert response.status_code == 200
    assert response.data["genre"] == [expected_genre]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_preferences",
    [
        ({}),  # Empty preferences
        ({"genreee": "comedy"}),  # Invalid field
    ],
)
def test_add_preferences_failure(new_preferences):
    user = UserFactory()
    client = APIClient()
    preferences_url = reverse("movies:user-preferences", kwargs={"user_id": user.id})
    # Attempt to add new preferences
    response = client.post(
        preferences_url, {"new_preferences": new_preferences}, format="json"
    )
    assert response.status_code == 400, response.json()


@pytest.mark.django_db
def test_add_and_retrieve_watch_history_with_movie_id() -> None:
    user = UserFactory()
    client = APIClient()
    watch_history_url = reverse(
        "movies:user-watch-history", kwargs={"user_id": user.id}
    )
    # Create movie instances using the MovieFactory
    movie1 = MovieFactory(
        title="The Godfather",
        release_year=1972,
        extra_data={"directors": ["Francis Ford Coppola"]},
        genres=["Crime", "Drama"],
    )
    movie2 = MovieFactory(
        title="Taxi Driver",
        release_year=1976,
        extra_data={"directors": ["Martin Scorsese"]},
        genres=["Crime", "Drama"],
    )
    # Add movies to watch history using their IDs
    for movie in [movie1, movie2]:
        response = client.post(watch_history_url, {"id": movie.id}, format="json")
        assert response.status_code == 201
        # Retrieve watch history to verify the addition
        response = client.get(watch_history_url)
        assert response.status_code == 200
    # This assumes your response includes the movie IDs in the watch history
    retrieved_movie_ids = [item["title"] for item in response.data["watch_history"]]
    for movie_title in [movie1.title, movie2.title]:
        assert movie_title in retrieved_movie_ids


@pytest.mark.django_db
def test_add_invalid_movie_id_to_watch_history() -> None:
    # Arrange: Create a user instance using Factory Boy
    user = UserFactory()
    client = APIClient()
    watch_history_url = reverse(
        "movies:user-watch-history", kwargs={"user_id": user.id}
    )
    # Act: Attempt to add a non-existent movie to the user's watch history
    invalid_movie_id = 99999  # Assuming this ID does not exist in the database
    response = client.post(
        watch_history_url, {"movie_id": invalid_movie_id}, format="json"
    )
    # Assert: Check for a 400 Bad Request response
    assert (
        response.status_code == 400
    ), "Expected a 400 Bad Request response for an invalid movie ID"


test_data = [
    (
        "file.csv",
        "text/csv",
        b'title,genres,extra_data\ntest,comedy,{"directors": ["name"]}\n',
        202,  # 201,
    ),  # Expected to succeed for CSV
    (
        "file.json",
        "application/json",
        b'[{"title": "test", "genres": ["comedy"], "extra_data": {"directors": ["name"]}}]',
        202,  # 201,
    ),  # Expected to succeed for JSON
    (
        "file.txt",
        "text/plain",
        b"This is a test.",
        400,
    ),  # Unsupported file type, expecting failure
]


@pytest.mark.parametrize(
    "file_name, content_type, file_content, expected_status", test_data
)
@pytest.mark.django_db
def test_general_upload_view(
    client: APIClient,
    file_name: str,
    content_type: str,
    file_content: str,
    expected_status: int,
):
    # Generate the URL dynamically using "reverse"
    url = reverse("movies:file-upload")
    # Create an in-memory uploaded file
    uploaded_file = SimpleUploadedFile(
        name=file_name, content=file_content, content_type=content_type
    )
    # Make a POST request to the GeneralUploadView endpoint
    response = client.post(url, {"file": uploaded_file}, format="multipart")
    # Assert that the response status code matches the expected status
    assert response.status_code == expected_status
