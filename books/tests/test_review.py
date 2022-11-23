import pytest
from rest_framework import status
from rest_framework.reverse import reverse

book_url = reverse("books-list")


@pytest.mark.django_db()
class TestCreateReview:
    def test_anonymous_can_not_write_review_return_401(self, api_client, create_book):
        response = api_client.post(f"{book_url}{create_book.id}/reviews/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_write_review_return_201(
        self,
        api_client,
        user_factory,
        create_book,
    ):
        user = user_factory.create(is_active=True)

        api_client.force_authenticate(user=user)

        response = api_client.post(
            f"{book_url}{create_book.id}/reviews/",
            {"description": "good book", "rating": 5},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_authenticated_user_can_not_write_two_reviews_return_400(
        self,
        api_client,
        user_factory,
        create_book,
    ):
        user = user_factory.create(is_active=True)

        api_client.force_authenticate(user=user)

        response = api_client.post(
            f"{book_url}{create_book.id}/reviews/",
            {"description": "good book", "rating": 5},
        )
        response = api_client.post(
            f"{book_url}{create_book.id}/reviews/",
            {"description": "good book 2", "rating": 3},
        )

        error = response.data[0]
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(error) == "You have already reviewed"

    def test_admin_user_can_write_review_return_200(
        self,
        api_client,
        user_factory,
        create_book,
    ):
        user = user_factory.create(is_staff=True)

        api_client.force_authenticate(user=user)

        response = api_client.post(
            f"{book_url}{create_book.id}/reviews/",
            {"description": "good book", "rating": 5},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_data_is_invalid_return_400(
        self,
        api_client,
        user_factory,
        create_book,
    ):
        user = user_factory.create(is_active=True)

        api_client.force_authenticate(user=user)

        response = api_client.post(
            f"{book_url}{create_book.id}/reviews/", {"description": "", "rating": 5}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestRetrieveReview:
    def test_anonymous_user_can_see_reviews_return_200(self, api_client, create_book):
        response = api_client.get(f"{book_url}{create_book.id}/reviews/")

        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_can_see_reviews_return_200(
        self, api_client, create_book, normal_user
    ):
        response = api_client.get(f"{book_url}{create_book.id}/reviews/")

        assert response.status_code == status.HTTP_200_OK

    def test_admin_user_can_see_reviews_return_200(
        self, api_client, create_book, admin_user
    ):
        response = api_client.get(f"{book_url}{create_book.id}/reviews/")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
class TestUpdateReview:
    def test_anonymous_user_can_not_update_review_return_401(
        self, api_client, create_book, user_factory, review_factory
    ):
        user = user_factory.create(is_active=True)
        create_review = review_factory.create(user=user, book=create_book)
        response = api_client.put(
            f"{book_url}{create_book.id}/reviews/{create_review.id}/"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_update_own_review_return_200(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user = user_factory.create(is_active=True)
        book = book_factory.create()
        api_client.force_authenticate(user)
        review = review_factory.create(book=book, user=user)

        response = api_client.put(
            f"{book_url}{book.id}/reviews/{review.pk}/",
            data={"description": "Updated Review", "rating": 4},
        )

        review.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert review.description == response.data["description"]
        assert review.rating == response.data["rating"]

    def test_authenticated_user_can_not_update_other_users_review_return_403(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user = user_factory.create_batch(is_active=True, size=2)
        user1 = user[0]
        user2 = user[1]

        book = book_factory.create()
        review = review_factory.create(book=book, user=user1)
        api_client.force_authenticate(user2)

        response = api_client.put(
            f"{book_url}{book.id}/reviews/{review.pk}/",
            data={"description": "Updated Review", "rating": 4},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_update_own_review_return_200(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user = user_factory.create(is_staff=True)
        book = book_factory.create()
        review = review_factory.create(book=book, user=user)
        api_client.force_authenticate(user)

        response = api_client.put(
            f"{book_url}{book.id}/reviews/{review.pk}/",
            data={"description": "Updated Review", "rating": 4},
        )

        review.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert review.description == response.data["description"]
        assert review.rating == response.data["rating"]

    def test_admin_user_can_update_other_users_review_return_200(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user1 = user_factory.create(is_active=True)
        user2 = user_factory.create(is_staff=True)

        book = book_factory.create()
        review = review_factory.create(book=book, user=user1)
        api_client.force_authenticate(user2)

        response = api_client.put(
            f"{book_url}{book.id}/reviews/{review.pk}/",
            data={"description": "Updated Review", "rating": 4},
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
class TestDeleteReview:
    def test_anonymous_user_can_not_delete_review_return_401(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user = user_factory.create(is_active=True)
        book = book_factory.create()

        review = review_factory.create(book=book, user=user)

        response = api_client.delete(f"{book_url}{book.id}/reviews/{review.pk}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_can_delete_own_review_return_204(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user = user_factory.create(is_active=True)
        book = book_factory.create()

        review = review_factory.create(book=book, user=user)
        api_client.force_authenticate(user)
        response = api_client.delete(f"{book_url}{book.id}/reviews/{review.pk}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_authenticated_user_can_not_delete_other_users_review_return_403(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user = user_factory.create_batch(is_active=True, size=2)
        user1 = user[0]
        user2 = user[1]

        book = book_factory.create()

        review = review_factory.create(book=book, user=user1)

        api_client.force_authenticate(user2)

        response = api_client.delete(f"{book_url}{book.id}/reviews/{review.pk}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_user_can_delete_own_review_return_204(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user = user_factory.create(is_staff=True)
        book = book_factory.create()

        review = review_factory.create(book=book, user=user)
        api_client.force_authenticate(user)

        response = api_client.delete(f"{book_url}{book.id}/reviews/{review.pk}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_admin_user_can_delete_other_users_review_return_204(
        self,
        api_client,
        user_factory,
        book_factory,
        review_factory,
    ):
        user1 = user_factory.create(is_staff=True)
        user2 = user_factory.create(is_active=True)

        book = book_factory.create()

        review = review_factory.create(book=book, user=user2)
        api_client.force_authenticate(user1)

        response = api_client.delete(f"{book_url}{book.id}/reviews/{review.pk}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
