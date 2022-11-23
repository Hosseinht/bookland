from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views



router = DefaultRouter()

router.register('authors', views.AuthorViewSet, basename='authors')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('books', views.BookViewSet, basename='books')

books_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
books_router.register('reviews', views.ReviewViewSet, basename='reviews')
# books_router.register('favorite', views.BookViewSet, basename='favorite')

# urlpatterns = [
#                   path('books/<int:pk>/favorite/', views.BookFavoriteViewSet.as_view()),
#               ] +

urlpatterns = router.urls + books_router.urls
