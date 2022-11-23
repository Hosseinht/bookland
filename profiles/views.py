from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .permissions import IsAdminOrAuthenticatedUserOrReadOnly
from .serializers import ProfileDetailSerializer, ProfileSerializer


class ProfileViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "head", "options"]
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrAuthenticatedUserOrReadOnly]
    lookup_field = "user__username"

    def retrieve(self, request, *args, **kwargs):
        context = {"request": request}
        try:
            queryset = Profile.objects.get(user__username=self.kwargs["user__username"])
            serializer = ProfileDetailSerializer(queryset, context=context)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile with this name doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
