from rest_framework import serializers
from nativo_english.api.shared.user.models import User
from django.contrib.auth.hashers import make_password

# Admin User Serializer
class AdminUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},  # Optional: hide password from output
        }

    def create(self, validated_data):
        # Set the password using the built-in method for hashing
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        # return super().create(validated_data)
        return user.save()
    


        