from typing import Optional
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes

from .models import Movie, UserMoviePreferences
from .serializers import MovieSerializer
from api_auth.permissions import CustomDjangoModelPermissions
from movies.serializers import AddPreferenceSerializer, AddToWatchHistorySerializer
from movies.services import (
    add_preference,
    user_preferences,
    add_watch_history,
    user_watch_history,
)
from recommendations.services import (
    UserPreferences,
    Item,
    get_recommendations,
    format_to_json,
)

# class MovieAPIView(views.APIView):
#     # get_object_or_404(MyModel, pk=1) is equivalent to:
#     # try:
#     #     obj = MyModel.objects.get(pk=1)
#     # except MyModel.DoesNotExist:
#     #     raise Http404("No MyModel matches the given query.")
#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, pk=None):
#         if pk:
#             # Retrieve a single movie
#             movie = get_object_or_404(Movie, pk=pk)
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#         else:
#             # List all movies
#             movies = Movie.objects.all()
#             serializer = MovieSerializer(movies, many=True)
#             return Response(
#                 {
#                     "count": len(serializer.data),
#                     "results": serializer.data,
#                     "next": None,
#                     "previous": None,
#                 }
#             )

#     def put(self, request, pk):
#         movie = get_object_or_404(Movie, pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         movie = get_object_or_404(Movie, pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# For listing all movies and creating a new movie
@extend_schema(
    summary="Retrieve all movies",
    description="Returns a paginated list of movies available in the system. Use filters and pagination parameters for large datasets.",
    responses={
        200: MovieSerializer(many=True),  # Response schema when successful
    },
    parameters=[
        OpenApiParameter("page", int, description="Page number for pagination"),
        OpenApiParameter("size", int, description="Page size for pagination"),
    ],
    methods=["GET"],  # Explicitly document GET
)
@extend_schema(
    summary="Create a new movie",
    description="Adds a new movie to the system. Requires authentication and appropriate permissions.",
    request=MovieSerializer,  # Request body schema for POST
    responses={
        201: MovieSerializer,  # Successful creation response schema
        400: OpenApiResponse(description="Bad Request. Validation error."),
        403: OpenApiResponse(description="Forbidden. Insufficient permissions."),
    },
    methods=["POST"],  # Explicitly document POST
)
@method_decorator(ratelimit(key="ip", rate="5/m", method="GET", block=True), name="get")
class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all().order_by("id")
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    summary="Update a movie by ID",
    description="Updates the details of an existing movie. Requires authentication and proper permissions.",
    request=MovieSerializer,  # Request body schema
    responses={
        200: MovieSerializer,  # Success response
        400: OpenApiResponse(description="Bad Request. Validation error."),
        403: OpenApiResponse(description="Forbidden. Insufficient permissions."),
        404: OpenApiResponse(description="Movie not found."),
    },
    parameters=[
        OpenApiParameter("id", int, description="ID of the movie to update"),
    ],
    methods=["GET"],
)
# For retrieving, updating, and deleting a single movie
@permission_classes([IsAuthenticated, CustomDjangoModelPermissions])
class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


@permission_classes([IsAuthenticated])
class UserPreferencesView(APIView):
    """
    View to add new user preferences and retrieve them.
    """

    def post(self, request: Request, user_id: int) -> Response:
        serializer = AddPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            add_preference(user_id, serializer.validated_data["new_preferences"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, user_id: int) -> Response:
        data = user_preferences(user_id)
        return Response(data)


@permission_classes([IsAuthenticated])
class WatchHistoryView(APIView):
    """
    View to retrieve and add movies to the user's watch history.
    """

    def get(self, request: Request, user_id: int) -> Response:
        data = user_watch_history(user_id)
        return Response(data)

    def post(self, request: Request, user_id: int) -> Response:
        serializer = AddToWatchHistorySerializer(data=request.data)
        if serializer.is_valid():
            add_watch_history(
                user_id,
                serializer.validated_data["id"],
            )
            return Response(
                {"message": "Movie added to watch history."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from contextlib import contextmanager
from django.core.files.storage import default_storage
from typing import Any
from movies.serializers import GeneralFileUploadSerializer
from movies.services import FileProcessor


@contextmanager
def temporary_file(uploaded_file):
    try:
        file_name = default_storage.save(uploaded_file.name, uploaded_file)
        file_path = default_storage.path(file_name)
        yield file_path
    finally:
        default_storage.delete(file_name)


from movies.tasks import process_file


# class GeneralUploadView(APIView):
#     def post(self, request, *args: Any, **kwargs: Any) -> Response:
#         serializer = GeneralFileUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             uploaded_file = serializer.validated_data["file"]
#             file_type = uploaded_file.content_type
#             with temporary_file(uploaded_file) as file_path:
#                 # processor = FileProcessor()
#                 # movies_processed = processor.process(file_path, file_type)
#                 # return Response(
#                 #     {"message": f"{movies_processed} movies processed successfully."},
#                 #     status=status.HTTP_201_CREATED,
#                 # )

#                 # Celery call using delay
#                 process_file.delay(file_path, file_type)
#                 return Response(
#                     {"message": f"Your file is being processed."},
#                     status=status.HTTP_202_ACCEPTED,
#                 )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GeneralFileUploadSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


@extend_schema(
    summary="Upload a CSV or JSON file for background processing",
    description=(
        "Uploads a CSV or JSON file and enqueues a background task for processing the file. "
        "The user must be authenticated. The file is saved with a unique name, "
        "and the task is asynchronously processed. Supported file types: CSV and JSON."
    ),
    request=GeneralFileUploadSerializer,  # Expected input for the file upload
    responses={
        202: OpenApiResponse(
            description="File uploaded successfully. Job enqueued for background processing.",
            examples={"application/json": {"message": "Job enqueued for processing."}},
        ),
        400: OpenApiResponse(
            description="Bad Request. Validation error or unsupported file type."
        ),
    },
    parameters=[
        OpenApiParameter(
            name="file", type="file", description="The CSV or JSON file to upload"
        ),
    ],
    methods=["POST"],  # Explicitly documents the POST method
)
@permission_classes([IsAuthenticated])
class GeneralUploadView(APIView):
    def post(self, request, *args: Any, **kwargs: Any) -> Response:
        serializer = GeneralFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data["file"]
            file_type = uploaded_file.content_type
            # Extract the file extension
            file_extension = os.path.splitext(uploaded_file.name)[1]
            # Generate a unique file name using UUID
            unique_file_name = f"{uuid.uuid4()}{file_extension}"
            # Save the file directly to the default storage
            file_name = default_storage.save(
                unique_file_name, ContentFile(uploaded_file.read())
            )
            uploaded_file.seek(0)
            process_file.delay(file_name, file_type)
            return Response(
                {"message": f"Job enqueued for processing."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieRecommendationAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return self._response_error(
                detail="user_id query parameter is required.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user_preferences = self._get_user_preferences(user_id)
        if not user_preferences:
            return self._response_error(
                detail="User preferences not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        recommended_items = self._get_recommended_items(user_preferences)
        response_data = self._format_response(recommended_items)
        return Response(response_data, status=status.HTTP_200_OK)

    def _get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """
        Retrieves user preferences from the database and converts them into the UserPreferences Pydantic model.
        :param user_id: The ID of the user whose preferences are to be fetched.
        :return: A UserPreferences object populated with the user's preferences, or None if no preferences exist.
        """
        try:
            # Fetch user preferences from the database
            user_prefs = UserMoviePreferences.objects.get(user_id=user_id)
            # Extracting the relevant preferences
            genre = user_prefs.preferences.get("genre", [])
            director = user_prefs.preferences.get("director", [])
            actor = user_prefs.preferences.get("actor", [])
            year_range = user_prefs.preferences.get("year", [])
            # Handle year range if it's provided (expecting a list)
            year_range_start, year_range_end = (
                (year_range[0], year_range[-1])
                if len(year_range) >= 2
                else (None, None)
            )
            # Build the preferences dictionary
            preferences_dict = {
                "genre": genre,
                "director": director,
                "actor": actor,
                "year_range_start": year_range_start,
                "year_range_end": year_range_end,
            }
            # Instantiate UserPreferences with the preferences dictionary
            return UserPreferences(
                preferences=preferences_dict,
                watch_history=user_prefs.watch_history,  # Assuming this exists in user_prefs
            )
        except UserMoviePreferences.DoesNotExist:
            return None  # Return None if no preferences are found for the user

    def _get_recommended_items(self, user_preferences: UserPreferences) -> list[Item]:
        """
        Generates a list of recommended items (in this case, movies) based on user preferences.
        :param user_preferences: The preferences of the user.
        :return: A list of recommended items as Item objects.
        """
        movies = Movie.objects.all()
        items = [
            Item(
                id=movie.id,
                attributes={
                    "name": movie.title,
                    "genre": movie.genres,
                    "director": movie.extra_data.get("directors", ""),
                    "year": movie.release_year,
                },
            )
            for movie in movies
        ]
        return get_recommendations(user_preferences=user_preferences, items=items)

    def _format_response(self, items: list[Item]) -> str:
        print(items)
        return format_to_json(items)
