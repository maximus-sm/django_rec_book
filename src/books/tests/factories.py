from factory.django import DjangoModelFactory
from factory.faker import Faker
from books.models import Book


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = Faker("sentence")
    author = Faker("name")
    isbn = Faker("isbn13")
    publication_date = Faker("date", pattern="%Y-%m-%d")
