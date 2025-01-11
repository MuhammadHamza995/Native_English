from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from nativo_english.api.shared.user.models import User, UserPrefs, OTP, TempToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
    


# LoginSerializer
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError({"detail": "Invalid credentials."})

        return {"user": user}  # Return the user for further handling in the view

class TwoFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrefs
        fields = ['enable_2fa']

    def update(self, instance, validated_data):
        instance.enable_2fa = validated_data.get('enable_2fa', instance.enable_2fa)
        # if instance.enable_2fa and not instance.otp_secret_key:
        #     instance.generate_otp_secret()  # Generate OTP secret key if enabling 2FA
        instance.save()
        return instance
    
class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['otp']



# Serializer for the Resend OTP request, only requiring user_id
class ResendOtpRequestSerializer(serializers.Serializer):
    temp_token = serializers.CharField()

# Serializer for logout
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()