import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from profiles.models import Profile

profile_url = reverse("profiles-list")





@pytest.mark.django_db()
class TestCreateProfile:
    def test_user_profile_is_created_return_200(
        self, api_client, admin_user, user_factory
    ):
        """
        After creating a user, signal will create a profile for that user. Here I create a user, then check
        if there is Profile related to that user
        """
        user = user_factory.create(is_active=True)

        profile = Profile.objects.get(user=user)

        response = api_client.get(f"{profile_url}{profile.user.username}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] > 0


@pytest.mark.django_db()
class TestRetrieveProfile:
    def test_anonymous_user_can_not_see_profile_list_return_401(self, api_client):
        response = api_client.get(profile_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_user_can_not_see_profile_of_a_user_return_401(
        self, api_client, user_factory
    ):
        user = user_factory.create(is_active=True)

        profile = Profile.objects.get(user=user)

        response = api_client.get(f"{profile_url}{profile.user.username}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_see_profile_list_return_200(
        self, api_client, normal_user
    ):
        response = api_client.get(profile_url)

        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_can_see_profile_of_a_user_return_200(
        self, api_client, user_factory, normal_user
    ):
        user = user_factory.create(is_active=True)

        profile = Profile.objects.get(user=user)

        response = api_client.get(f"{profile_url}{profile.user.username}/")

        assert response.status_code == status.HTTP_200_OK

    def test_admin_user_can_see_profile_list_return_200(self, api_client, normal_user):
        response = api_client.get(profile_url)

        assert response.status_code == status.HTTP_200_OK

    def test_admin_user_can_see_profile_of_a_user_return_200(
        self, api_client, user_factory, admin_user
    ):
        user = user_factory.create(is_active=True)

        profile = Profile.objects.get(user=user)

        response = api_client.get(f"{profile_url}{profile.user.username}/")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
class TestUpdateReview:
    def test_anonymous_user_can_not_update_profile_return_401(
        self,
        api_client,
        user_factory,
    ):
        user = user_factory.create(is_active=True)

        profile = Profile.objects.get(user=user)

        response = api_client.patch(f"{profile_url}{profile.user.username}/")
        print(response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_update_own_profile_return_200(
        self,
        api_client,
        user_factory,
    ):
        user = user_factory.create(is_active=True)
        profile = Profile.objects.get(user=user)

        api_client.force_authenticate(user)

        response = api_client.patch(
            f"{profile_url}{profile.user.username}/",
            {
                "email": "newemail@gmail.com",
                "first_name": "John",
                "last_name": "Smith",
                "phone": "+989122823645",
                "birth_date": "2021-09-04",
                "about": "about",
            },
        )

        profile.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert profile.user.email == response.data["email"]
        assert profile.user.first_name == response.data["first_name"]
        assert profile.user.last_name == response.data["last_name"]
        assert profile.phone == response.data["phone"]
        assert profile.birth_date.strftime("%Y-%m-%d") == response.data["birth_date"]
        assert profile.about == response.data["about"]

    def test_authenticated_user_can_not_update_another_user_profile_return_403(
        self,
        api_client,
        user_factory,
    ):
        user = user_factory.create_batch(is_active=True, size=2)
        user1 = user[0]
        user2 = user[1]

        profile = Profile.objects.get(user=user1)
        api_client.force_authenticate(user2)

        response = api_client.patch(
            f"{profile_url}{profile.user.username}/",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_update_own_profile_return_200(
        self,
        api_client,
        user_factory,
    ):
        user = user_factory.create(is_staff=True)
        profile = Profile.objects.get(user=user)

        api_client.force_authenticate(user)

        response = api_client.patch(
            f"{profile_url}{profile.user.username}/",
            {
                "email": "newemail@gmail.com",
                "first_name": "John",
                "last_name": "Smith",
                "phone": "+989122823645",
                "birth_date": "2021-09-04",
                "about": "about",
            },
        )

        assert response.status_code == status.HTTP_200_OK

    def test_admin_user_can_update_another_user_profile_return_200(
        self, api_client, user_factory
    ):
        user1 = user_factory.create(is_active=True)
        user2 = user_factory.create(is_staff=True)

        profile = Profile.objects.get(user=user1)

        api_client.force_authenticate(user2)

        response = api_client.patch(
            f"{profile_url}{profile.user.username}/",
            {
                "email": "newemail@gmail.com",
                "first_name": "John",
                "last_name": "Smith",
                "phone": "+989122823645",
                "birth_date": "2021-09-04",
                "about": "about",
            },
        )

        assert response.status_code == status.HTTP_200_OK
