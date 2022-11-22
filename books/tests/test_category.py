import pytest
from rest_framework import status
from rest_framework.reverse import reverse

category_url = reverse("categories-list")


@pytest.mark.django_db()
class TestCreateCategory:
    def test_anonymous_user_can_not_create_category_return_401(self, api_client):
        response = api_client.post(category_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_can_not_create_category_return_403(
        self, api_client, normal_user
    ):
        response = api_client.post(category_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_create_category_return_201(
        self,
        api_client,
        admin_user,
        create_category,
    ):
        response = api_client.post(category_url, {"name": "a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_data_is_invalid_return_400(self, settings, api_client, admin_user):
        response = api_client.post(category_url, {"name": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["name"] is not None


@pytest.mark.django_db()
class TestRetrieveCategory:
    def test_anonymous_user_can_not_see_list_of_categories_return_401(self, api_client):
        response = api_client.get(category_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_user_can_not_see_a_single_category_return_401(
        self, api_client, create_category
    ):
        response = api_client.get(f"{category_url}{create_category.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_user_can_not_see_list_of_categories_return_403(
        self, api_client, normal_user
    ):
        response = api_client.get(category_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_admin__user_can_not_see_list_of_categories_return_403(
        self, api_client, normal_user, create_category
    ):
        response = api_client.get(f"{category_url}{create_category.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_user_can_see_list_of_categories_return_200(
        self, api_client, admin_user
    ):
        response = api_client.get(category_url)
        assert response.status_code == status.HTTP_200_OK

    def test_if_normal_user_can_see_a_single_author_return_200(
        self, api_client, admin_user, create_category
    ):
        response = api_client.get(f"{category_url}{create_category.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == create_category.id
        assert response.data["name"] == create_category.name


@pytest.mark.django_db()
class TestUpdateAuthor:
    def test_anonymous_user_can_not_update_category_return_401(
        self, api_client, create_category
    ):
        response = api_client.put(f"{category_url}{create_category.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_user_can_not_update_category_return_403(
        self, api_client, normal_user, create_category
    ):
        response = api_client.put(f"{category_url}{create_category.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_update_category_return_200(
        self,
        api_client,
        create_category,
        admin_user,
    ):
        payload = {"name": "a"}
        response = api_client.patch(f"{category_url}{create_category.id}/", payload)

        create_category.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert create_category.name == payload["name"]


class TestDeleteAuthor:
    def test_anonymous_user_can_not_delete_category_return_401(
        self, api_client, create_category
    ):
        response = api_client.delete(f"{category_url}{create_category.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_user_can_not_delete_category_return_403(
        self, api_client, normal_user, create_category
    ):
        response = api_client.delete(f"{category_url}{create_category.id}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_delete_category_return_403(
        self, api_client, admin_user, create_category
    ):
        response = api_client.delete(f"{category_url}{create_category.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
