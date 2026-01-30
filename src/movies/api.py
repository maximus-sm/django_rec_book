from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import Movie
from .serializers import MovieSerializer
from django.shortcuts import get_object_or_404
from movies.serializers import AddPreferenceSerializer, AddToWatchHistorySerializer
from movies.services import (
    add_preference,
    user_preferences,
    add_watch_history,
    user_watch_history,
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
class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all().order_by("id")
    serializer_class = MovieSerializer


# For retrieving, updating, and deleting a single movie
class MovieDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


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
            process_file.delay(file_name, file_type)
            return Response(
                {"message": f"Job enqueued for processing."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
