from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileUpdateSerializer(serializers.ModelSerializer):
    User = UserSerializers(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'