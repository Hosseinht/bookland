from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('authors', views.AuthorViewSet)
router.register('books', views.BookViewSet)
router.register('reviews', views.ReviewViewSet)

urlpatterns = router.urls
