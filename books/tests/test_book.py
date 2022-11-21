import os
import shutil

import pytest
from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse

# User = get_user_model()

book_url = reverse("books-list")

TEST_DIR = "books/tests/test_data/"
# For Docker and linux

WIN_TEST_DIR = "test_data/"
# For windows

path = settings.BASE_DIR
file_path = os.path.join(path, "books/tests/test_data/media/books/images/")


@pytest.mark.django_db()
class TestCreateBook:
    def test_anonymous_cant_create_book_return_401(self, api_client):
        response = api_client.post(book_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_cant_create_book_return_403(
        self, api_client, normal_user
    ):
        response = api_client.post(book_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @override_settings(MEDIA_ROOT=(WIN_TEST_DIR + "/media"))
    def test_admin_can_create_book_return_200(
        self, api_client, admin_user, create_book, book_payload
    ):

        response = api_client.post("/api/v1/books/", book_payload)
        print(response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        shutil.rmtree(file_path)
        # if using windows

        # shutil.rmtree('books/tests/test_data/media/books/images/')
        # if using docker or linux


# class TestRetrieveBook:
