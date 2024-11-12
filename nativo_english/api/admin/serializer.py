from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

# Admin User Serializer
class AdminUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])  # Applying custom username validator
    password = serializers.CharField(write_only=True, validators=[validate_password])  # Applying custom password validator

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'first_name', 'last_name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password from output
        }

    def create(self, validated_data):
        # Apply password hashing
        if validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])
            user = User(**validated_data)

            # Save the user instance
            user.save()
            return user  # Return the user object after saving
        
        user = User.objects.create(**validated_data)  # Save and create user
        return user

    def validate(self, data):
        """
        Validate the entire input data dictionary, and provide custom error messages for missing or incorrect fields.
        """
        if not data.get("username"):
            raise ValidationError({"status": "error", "message": "Username is required.", "data": None})
        if not data.get("password"):
            raise ValidationError({"status": "error", "message": "Password is required.", "data": None})

        return data
