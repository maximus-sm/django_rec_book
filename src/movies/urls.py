from django.urls import path

# from movies.api import MovieAPIView
from .api import (
    MovieListCreateAPIView,
    MovieDetailAPIView,
    UserPreferencesView,
    WatchHistoryView,
    GeneralUploadView,
)

app_name = "movies"  # Define the application namespace
# urlpatterns = [
#     path("movies/", MovieAPIView.as_view(), name="movie-api"),
#     path("movies/<int:pk>", MovieAPIView.as_view(), name="movie-api-detail"),
# ]


urlpatterns = [
    path("movies/", MovieListCreateAPIView.as_view(), name="movie-list"),
    path("movies/<int:pk>/", MovieDetailAPIView.as_view(), name="movie-detail"),
    path(
        "user/<int:user_id>/preferences/",
        UserPreferencesView.as_view(),
        name="user-preferences",
    ),
    path(
        "user/<int:user_id>/watch-history/",
        WatchHistoryView.as_view(),
        name="user-watch-history",
    ),
    path("upload/", GeneralUploadView.as_view(), name="file-upload"),
]
