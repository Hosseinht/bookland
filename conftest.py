import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register
from rest_framework.test import APIClient

from books.tests.factories import (AuthorFactory, BookFactory, CategoryFactory,
                                   UserFactory, ReviewFactory)

register(UserFactory)
register(AuthorFactory)
register(CategoryFactory)
register(BookFactory)
register(ReviewFactory)

User = get_user_model()


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def admin_user(api_client):
    return api_client.force_authenticate(user=User(is_staff=True))


@pytest.fixture()
def normal_user(api_client):
    return api_client.force_authenticate(user=User(is_active=True))


@pytest.fixture()
def create_category(db, category_factory):
    create_category = category_factory.create()
    return create_category


@pytest.fixture()
def create_author(db, author_factory):
    create_author = author_factory.create()
    return create_author


@pytest.fixture()
def create_book(db, book_factory):
    create_book = book_factory.create()
    return create_book


@pytest.fixture()
def book_payload(db, create_book, create_author):
    author = create_author
    return {
        "id": create_book.id,
        "author": author,
        "category": create_book.category,
        "title": "title",
        "description": "description",
        "price": create_book.price,
        "publisher": "publisher",
        "language": "English",
        "pages": 120,
        "isbn": create_book.isbn,
        "cover_image": create_book.cover_image,
    }


@pytest.fixture()
def invalid_book_payload(db, create_book, create_author):
    author = create_author
    return {
        "id": create_book.id,
        "author": author,
        "category": create_book.category,
        "title": "",
        "description": "description",
        "price": 32.32,
        "publisher": "publisher",
        "language": "English",
        "pages": 120,
        "isbn": create_book.isbn,
        "cover_image": create_book.cover_image,
    }


@pytest.fixture()
def author_payload(db):
    author = {
        "id": 2,
        "name": "John Smith",
        "pseudonym": "Johns",
        "about": "about",
    }

    return author


@pytest.fixture()
def create_author(db, author_factory):
    create_author = author_factory.create()
    return create_author


@pytest.fixture()
def create_review(db, review_factory, user_factory):
    user = user_factory.create(is_active=True)
    create_review = review_factory.create(user=user)
    return create_review

