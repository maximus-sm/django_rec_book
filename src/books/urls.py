from django.urls import path, include
from .views import BookListCreateAPIView, BookDetailAPIView

app_name = "books"
urlpatterns = [
    path("books/", BookListCreateAPIView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailAPIView.as_view(), name="book-detail"),
]
