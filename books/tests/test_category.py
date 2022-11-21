import pytest
from rest_framework import status
from rest_framework.reverse import reverse

# User = get_user_model()

author_url = reverse("authors-list")
author_detail_url = reverse("authors-detail", kwargs={"pk": 1})


@pytest.mark.django_db()
class TestRetrieveAuthor:
    def test_if_anonymous_user_can_see_authors_return_200(self, api_client):
        response = api_client.get(author_url)

        assert response.status_code == status.HTTP_200_OK

    def test_if_normal_user_can_see_authors_return_200(self, api_client, normal_user):
        response = api_client.get(author_url)
        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_user_can_see_authors_return_200(self, api_client, admin_user):
        response = api_client.get(author_url)
        assert response.status_code == status.HTTP_200_OK

    def test_if_normal_user_can_see_a_single_author_return_200(
        self, api_client, create_author
    ):
        response = api_client.get(f"{author_url}{create_author.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == create_author.id
        assert response.data["name"] == create_author.name
        assert response.data["pseudonym"] == create_author.pseudonym
        assert response.data["about"] == create_author.about


@pytest.mark.django_db()
class TestCreateAuthor:
    def test_anonymous_user_cant_create_author_return_401(self, api_client):
        response = api_client.post(author_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_cant_create_author_return_403(self, api_client, normal_user):
        response = api_client.post(author_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_create_author_return_201(
        self, api_client, admin_user, create_book, create_author
    ):
        response = api_client.post(author_url, {"name": "a"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db()
class TestUpdateAuthor:
    def test_anonymous_user_cant_update_author_return_401(
        self, api_client, create_author
    ):
        response = api_client.put(f"{author_url}{create_author.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_user_can_update_author_return_200(
        self, api_client, create_author, admin_user, author
    ):
        response = api_client.patch(f"{author_url}{create_author.id}/", author)
        # here the data that is created by the create_author will be updated with the data that is in the author

        create_author.refresh_from_db()
        # without doing this create_author data remain the same and won't be updated with the author data

        assert response.status_code == status.HTTP_200_OK
        assert create_author.name == author["name"]
        assert create_author.pseudonym == author["pseudonym"]
        assert create_author.about == author["about"]
