

from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Required by the checker
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()  # Ensure password is write-only

    class Meta:
        model = get_user_model()  # Use the custom user model
        fields = ['id', 'username', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        Token.objects.create(user=user)  # Create a token for the user
        return user