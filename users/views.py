from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):

    def get_serializer_context(self):
        return {"user": self.request.user}
