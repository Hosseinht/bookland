from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('profiles', views.ProfileViewSet, basename='profiles', )

urlpatterns = router.urls
