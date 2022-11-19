from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers


from books.urls import router as books_router
from profiles.urls import router as profiles_router

router = routers.DefaultRouter()
router.registry.extend(books_router.registry)
router.registry.extend(profiles_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/', include(router.urls)),
    path('api/v1/', include('books.urls')),

    path('api/auth/', include('users.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
