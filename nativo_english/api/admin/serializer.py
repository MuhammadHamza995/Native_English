from rest_framework import serializers
from nativo_english.api.shared.user.models import User
from .models import CourseImage

# Admin User Serializer
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'first_name', 'last_name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password from output
        }

# Course Image Serializer
class CourseImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)  # Explicitly define the image field for file upload

    class Meta:
        model = CourseImage
        fields = ['id', 'name', 'image']
