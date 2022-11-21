from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import ProfileSerializer, ProfileDetailSerializer
from django.contrib.auth import get_user_model
from .permissions import IsAdminOrAuthenticatedUserOrReadOnly

User = get_user_model()


class ProfileViewSet(ModelViewSet):
    http_method_names = ["get", "put", "patch", "delete", "head", "options"]
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrAuthenticatedUserOrReadOnly]
    lookup_field = 'user__username'

    def retrieve(self, request, *args, **kwargs):
        context = {'request': request}
        queryset = Profile.objects.get(user__username=self.kwargs['user__username'])
        serializer = ProfileDetailSerializer(queryset, context=context)
        return Response(serializer.data)
