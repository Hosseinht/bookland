import os
import shutil

import pytest
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

book_url = reverse("books-list")

# TEST_DIR = "books/tests/test_data/media/"
# For Docker and linux

# WIN_TEST_DIR = "books/tests/test_data/media/"
# For windows

path = settings.BASE_DIR
file_path = os.path.join(path, "books/tests/test_data/media/books/images/")
TEST_DIR = os.path.join(path, "books/tests/test_data/media/")


@pytest.mark.django_db()
class TestCreateBook:
    def test_anonymous_can_not_create_book_return_401(self, api_client):
        response = api_client.post(book_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_user_can_not_create_book_return_403(
        self, api_client, normal_user
    ):
        response = api_client.post(book_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_create_book_return_200(
        self, settings, api_client, admin_user, create_book, book_payload
    ):
        settings.MEDIA_ROOT = TEST_DIR

        response = api_client.post(book_url, book_payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

        shutil.rmtree(file_path)

    def test_data_is_invalid_return_400(
        self, settings, api_client, admin_user, invalid_book_payload
    ):
        settings.MEDIA_ROOT = TEST_DIR

        response = api_client.post(book_url, invalid_book_payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None


@pytest.mark.django_db()
class TestRetrieveBook:
    def test_anonymous_user_can_see_list_of_books_return_200(self, api_client):
        response = api_client.get(book_url)

        assert response.status_code == status.HTTP_200_OK

    def test_anonymous_user_can_see_a_single_book_return_200(
        self, api_client, create_book
    ):
        response = api_client.get(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_non_admin_user_can_see_list_of_books_return_200(
        self, api_client, normal_user
    ):
        response = api_client.get(book_url)

        assert response.status_code == status.HTTP_200_OK

    def test_non_admin_user_can_see_a_single_book_return_200(
        self, api_client, normal_user, create_book
    ):
        response = api_client.get(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_admin_user_can_see_list_of_books_return_200(self, api_client, admin_user):
        response = api_client.get(book_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_user_can_see_a_single_books_return_200(
        self, api_client, admin_user, create_book
    ):
        response = api_client.get(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_if_book_exist_return_200(
        self, api_client, admin_user, create_author, create_book
    ):
        author = create_author
        book = create_book
        book.author.add(author)
        # ManyToMany field

        author_name = book.author.all()
        author_name = author_name[0].name

        response = api_client.get(f"/api/v1/books/{book.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == book.id
        assert response.data["author"][0] == author_name
        assert response.data["category"] == book.category.name
        assert response.data["description"] == book.description
        assert response.data["price"] == book.price
        assert response.data["publisher"] == book.publisher
        assert response.data["language"] == book.language
        assert response.data["pages"] == book.pages
        assert response.data["isbn"] == book.isbn
        assert (
            response.data["cover_image"]
            == f"http://testserver/media/{book.cover_image}"
        )


@pytest.mark.django_db()
class TestUpdateBook:
    def test_anonymous_user_can_not_update_book_return_401(
        self, api_client, create_book
    ):
        response = api_client.put(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_user_can_not_update_book_return_401(
        self, api_client, create_book, normal_user
    ):
        response = api_client.put(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    # @override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
    def test_admin_user_can_update_book_return_200(
        self, settings, api_client, admin_user, create_book, create_author, book_payload
    ):
        settings.MEDIA_ROOT = TEST_DIR

        author = create_author
        book = create_book
        book.author.add(author)
        # ManyToMany field

        response = api_client.put(f"{book_url}{book.id}/", book_payload)

        book.refresh_from_db()

        author_name = book.author.all()

        assert response.status_code == status.HTTP_200_OK
        assert author_name[0] == book_payload["author"]
        assert book.category == book_payload["category"]
        assert book.title == book_payload["title"]
        assert book.description == book_payload["description"]
        assert book.price == book_payload["price"]
        assert book.publisher == book_payload["publisher"]
        assert book.language == book_payload["language"]
        assert book.pages == book_payload["pages"]
        assert int(book.isbn) == book_payload["isbn"]
        # assert book.cover_image == book_payload['cover_image']

        # delete test image after the test is done
        shutil.rmtree(file_path)


@pytest.mark.django_db()
class TestDeleteBook:
    def test_anonymous_user_can_not_delete_book_return_401(
        self, api_client, create_book
    ):
        response = api_client.delete(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_user_can_not_delete_book_return_403(
        self, api_client, normal_user, create_book
    ):
        response = api_client.delete(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_delete_book_return_204(
        self, api_client, admin_user, create_book
    ):
        response = api_client.delete(f"{book_url}{create_book.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
