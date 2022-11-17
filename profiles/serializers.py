from rest_framework import serializers

from users.serializers import CurrentUserSerializer
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        user_ser = CurrentUserSerializer(instance=user, data=user_data)
        if user_ser.is_valid():
            user_ser.save()

        instance.phone = validated_data.get('phone', instance.phone)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.about = validated_data.get('about', instance.about)
        instance.save()
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
