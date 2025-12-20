import pytest
from books.models import Book
from books.serializers import BookSerializer
import datetime

@pytest.mark.django_db
def test_book_serializer_valid_data():
    data = {"title":"New orlean","author":"John Dean","isbn":"0141439747","publication_date":"2001-12-12"}
    serializer = BookSerializer(data=data)
    assert serializer.is_valid()
    serializer.save()
    assert Book.objects.count() == 1
    saved = Book.objects.get()
    assert saved.title == data["title"]
    assert saved.author == data["author"]
    assert saved.isbn == data["isbn"]
    assert saved.publication_date == datetime.datetime.strptime(data["publication_date"],"%Y-%m-%d").date()

@pytest.mark.django_db
def test_book_serializer_invalid_data():
    data = {"isbn":"978-0141439747","publication_date":"2001-12-12"}
    serializer = BookSerializer(data=data)
    assert not serializer.is_valid()
    assert "author" in serializer.errors
    assert "title" in serializer.errors

@pytest.mark.django_db
def test_serialize_movie_instance():
    # Given a book instance
    book = Book.objects.create(
        title="Baltiomore Tales", author="Lester Freamon", isbn="5930940394",publication_date ="2012-08-19" 
    )
    # When we serialize the book
    serializer = BookSerializer(book)
    # Then the resulting JSON data should contain the book's details
    assert serializer.data == {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn" : book.isbn,
        "publication_date": book.publication_date,
    }


    
    