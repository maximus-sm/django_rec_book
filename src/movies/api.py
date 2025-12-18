from rest_framework import status, views, generics
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer
from django.shortcuts import get_object_or_404


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



