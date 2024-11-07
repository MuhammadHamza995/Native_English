from rest_framework import serializers
from nativo_english.api.shared.user.models import User
from django.contrib.auth.hashers import make_password

# Admin User Serializer
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'first_name', 'last_name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},  # Optional: hide password from output
        }

    def create(self, validated_data):
        if validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])
        
        user = User.objects.create(**validated_data)  # Save and create user

        return user