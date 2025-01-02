from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from nativo_english.api.shared.user.models import User, UserPrefs

# Admin User Serializer
class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'first_name', 'last_name', 'is_active', 'email']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password from output
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Create the default UserPrefs after the user is created
        UserPrefs.objects.create(fk_user_id=user)

        return user

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value