import pytest
from rest_framework import status
from django.urls import reverse
from books.models import Book
from .factories import BookFactory


@pytest.mark.django_db
def test_create_book(client):
    data = {
        "title": "Oliver Twist",
        "author": "Charles Dickens",
        "isbn": "978-0141439747",
        "publication_date": "2003-04-29",
    }
    url = reverse("books:book-list")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.filter(title=data["title"]).count() == 1


@pytest.mark.django_db
def test_book_factory():
    book = BookFactory()
    assert Book.objects.filter(id=book.id).count() == 1


@pytest.mark.django_db
def test_delete_book(client):
    book = BookFactory()
    # assert Book.objects.filter(id=book.id).exists()
    url = reverse("books:book-detail", kwargs={"pk": book.id})
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_retrieve_book(client):
    book = BookFactory()
    # assert Book.objects.filter(id=book.id).exists()
    url = reverse("books:book-detail", kwargs={"pk": book.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "publication_date": book.publication_date,
    }


@pytest.mark.django_db
def test_update_book_title(client):
    book = BookFactory()
    assert Book.objects.filter(id=book.id).exists()
    new_title = "New title"
    data = {"title": new_title}
    url = reverse("books:book-detail", kwargs={"pk": book.id})
    response = client.patch(url, data=data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    updated = Book.objects.filter(id=book.id)[0]
    assert updated
    assert updated.title == new_title
