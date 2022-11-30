from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

# from books.urls import router as books_router
# from profiles.urls import router as profiles_router

# router = routers.DefaultRouter()
# router.registry.extend(books_router.registry)
# router.registry.extend(profiles_router.registry)


schema_view = get_schema_view(
    openapi.Info(
        title="bookland",
        default_version="v1",
        description="Bookland is a bookstore based on Django rest framework",
        terms_of_service="https://www.myapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapp.local"),
        license=openapi.License(name="Good License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/v1/', include(router.urls)),
    path("api/v1/", include("books.urls")),
    path("api/v1/", include("profiles.urls")),
    path("api/auth/", include("users.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
