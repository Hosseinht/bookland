from django.db import transaction
from rest_framework import serializers

from users.serializers import CurrentUserSerializer
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = instance.user

            user_ser = CurrentUserSerializer(instance=user, data=user_data)
            if user_ser.is_valid():
                user_ser.save()

            return super().update(instance, validated_data)

    class Meta:
        model = Profile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'birth_date',
            'about',

        ]
