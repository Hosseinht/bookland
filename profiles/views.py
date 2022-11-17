from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import ProfileSerializer
from .permissions import CurrentUserOrAdmin


class ProfileViewSet(ModelViewSet):
    http_method_names = ["get", "put", "delete", "head", "options"]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CurrentUserOrAdmin]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if self.action == "list" and not user.is_staff:
            queryset = queryset.filter(user_id=user.pk)
        return queryset

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):

        profile = Profile.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = ProfileSerializer(profile, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
