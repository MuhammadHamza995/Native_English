from rest_framework import serializers
from nativo_english.api.shared.user.models import User
from nativo_english.api.admin.models import CourseImage

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
    image = serializers.ImageField(required=True)  # This handles the uploaded image
    image_url = serializers.SerializerMethodField()  # Field to show the image URL

    class Meta:
        model = CourseImage
        fields = ['id', 'image', 'image_url']  # Include the image_url field

    def get_image_url(self, obj):
        # This assumes that your image files are being served by Django’s static files mechanism.
        # If you're using something like AWS S3, you'll need to generate the URL based on that.
        return obj.image.url if obj.image else None

