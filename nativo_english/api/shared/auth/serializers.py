from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from nativo_english.api.shared.user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from nativo_english.api.shared.utils import api_exception_handler

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

# # Login Serializer
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         user = authenticate(username=attrs['username'], password=attrs['password'])

#         # Check for user
#         if not user:
#             raise serializers.ValidationError('Invalid credentials')
        
#         attrs['user'] = user
#         return attrs
    

# Token Serializer
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            
            # Get both refresh and access tokens
            refresh = self.get_token(self.user)
            access = refresh.access_token

            # Custom payload with user information
            data['refresh'] = str(refresh)
            data['access'] = str(access)
            data['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role  # Assuming `role` is a field on your User model
            }
            
            return data
        
        except ValidationError as e:
            print("---------------------------------")
            print(str(e))
            print("---------------------------------")
            # Handle validation errors specifically
            raise ValidationError({"detail": str(e)})
        
        except Exception as ex:
            # Log the exception and raise a generic error
            print("---------------------------------")
            print(str(ex))
            print("---------------------------------")
            
            raise ValidationError({
                "detail": "An error occurred during login.",
                'error': str(ex)
                })