from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, TwoFactorSerializer, VerifyOTPSerializer, ResendOtpRequestSerializer, LogoutSerializer, ForgotPasswordSerializer
from nativo_english.api.shared.utils import api_response
from rest_framework.views import APIView
from nativo_english.api.shared.user.models import UserPrefs, OTP, User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .swagger_schema import (FA2_UPDATE_SCHEMA, VERIFY_OTP_SCHEMA,RESEND_OTP_SCHEMA,FORGOT_PASSWORD_SCHEMA,UPDATE_PASSWORD_SCHEMA)

def generate_jwt_tokens(user):
    """
    Generate JWT refresh and access tokens with custom claims for a user.
    """
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    # Add custom claims to the access token
    access['role'] = user.role
    access['email'] = user.email
    access['username'] = user.username

    return {
        "refresh": str(refresh),
        "access": str(access)
    }


# Create your views here.

# RegisterView for Registration API
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# LoginView for Login APIclass LoginView(TokenObtainPairView):
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Check if 2FA is enabled for the user
        user_prefs = UserPrefs.objects.filter(fk_user_id=user).first()
        if user_prefs and user_prefs.enable_2fa:
            
            OTP.objects.filter(user=user, is_used=False).update(is_used=True)

           
            otp_obj = OTP(user=user)
            otp_obj.generate_otp()

            # Create a temporary token
            temp_token = RefreshToken.for_user(user).access_token
            temp_token["temp"] = True
            temp_token["user_id"] = user.id
            temp_token["role"] = user.role
            temp_token.set_exp(lifetime=timedelta(minutes=5))

            return api_response(
                status.HTTP_200_OK,
                message="2FA is enabled. Use the temporary token to verify the OTP.",
                data={
                    "temp_token": str(temp_token),
                    "is_2fa_enabled": True,
                    "user_id": user.id,
                    "role": user.role
                },
            )

        # Generate JWT tokens if 2FA is not enabled
        tokens = generate_jwt_tokens(user)
        tokens["is_2fa_enabled"] = False
        tokens["user_id"] = user.id
        tokens["role"] = user.role

        return api_response(status.HTTP_200_OK, "Login Successful", data=tokens)




# TWO FA VIEW
class TwoFactorView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TwoFactorSerializer

    @extend_schema(**FA2_UPDATE_SCHEMA)
    def patch(self, request, *args, **kwargs):
        # Retrieve the user's preferences
        user_pref, created = UserPrefs.objects.get_or_create(
            fk_user_id=request.user
        )

        user_pref.enable_2fa = request.data['enable_2fa']
        user_pref.save()

        # Use the serializer to validate and update the user's preferences
        serializer = self.serializer_class(user_pref, data=request.data, partial=True)

        if serializer.is_valid():
            # Save the updated preferences
            serializer.save()
            return api_response(status.HTTP_200_OK, message='2FA settings updated successfully.', data=serializer.data)
            
        return api_response(status.HTTP_400_BAD_REQUEST, message=serializer.errors)


# Verify OTP View
class VerifyOtpView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyOTPSerializer

    @extend_schema(**VERIFY_OTP_SCHEMA)
    def post(self, request, *args, **kwargs):
        otp_input = request.data.get("otp")

        # Validate the token
        from rest_framework_simplejwt.authentication import JWTAuthentication
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return api_response(status.HTTP_400_BAD_REQUEST, message="No bearer token passed in Authorization header")

        temp_token_value = auth_header.split(" ")[1]
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(temp_token_value)
        user_id = validated_token.get("user_id")

        # Fetch OTP and validate
        otp_obj = OTP.objects.filter(user_id=user_id, otp=otp_input, is_used=False).first()
        if not otp_obj or not otp_obj.is_valid():
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                "Invalid or expired OTP."
            )

        # Mark OTP as used
        otp_obj.is_used = True
        otp_obj.save()

        # Get user object
        user = User.objects.get(id=user_id)

        # Generate JWT tokens upon successful OTP verification
        tokens = generate_jwt_tokens(user)
        tokens["user_id"] = user.id
        tokens["role"] = user.role

        return api_response(
            status.HTTP_200_OK,
            message="OTP verified successfully.",
            data=tokens
        )



# This function will check for token present in Authorization header or not
def is_token_present_in_header(request):
    auth_header = request.headers.get('Authorization')
    
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]

    # If no token or invalid header, return None
    return None



# Resend the OTP to the user 
class ResendOtpView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResendOtpRequestSerializer  # Use the serializer for the POST request

    @extend_schema(**RESEND_OTP_SCHEMA)  # Extend the schema for the API documentation
    def post(self, request, *args, **kwargs):
    # Validate request body using the ResendOtpRequestSerializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            temp_token = serializer.validated_data["temp_token"]

            # Validate the token
            from rest_framework_simplejwt.authentication import JWTAuthentication
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return api_response(status.HTTP_400_BAD_REQUEST, message="No bearer token passed in Authorization header")

            temp_token_value = auth_header.split(" ")[1]
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(temp_token_value)
            user_id = validated_token.get("user_id")

            # Check if the user exists
            user = User.objects.filter(id=user_id).first()
            if not user:
                return api_response(
                    status.HTTP_404_NOT_FOUND,
                    message="User not found."
                )

            # Check if 2FA is enabled for the user
            user_prefs = UserPrefs.objects.filter(fk_user_id=user).first()
            if not user_prefs or not user_prefs.enable_2fa:
                return api_response(
                    status.HTTP_400_BAD_REQUEST,
                    message="User does not have 2FA enabled."
                )

            # Mark previous OTPs as used
            previous_otps = OTP.objects.filter(user=user, is_used=False)
            previous_otps.update(is_used=True)

            # Generate OTP
            # otp_obj = OTP.objects.create(user=user)
            # otp_obj.generate_otp()
            otp_obj = OTP(user=user)
            otp_obj.generate_otp()

            # Include role in response
            role = user.role  # Directly access the role field

            return api_response(
                status.HTTP_200_OK,
                message="OTP has been resent successfully.",
                data={
                    "temp_token": str(temp_token),
                    "user_id": user.id,
                    "role": role
                }
            )

        return api_response(
            status.HTTP_400_BAD_REQUEST, message=serializer.errors
        
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer  # Use the serializer for the POST request

    def post(self, request, *args, **kwargs):
        # try:
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return api_response(status.HTTP_400_BAD_REQUEST, message="Refresh token is required")
            
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()

        return api_response(status.HTTP_200_OK, message="Logout successful")
        # except TokenError as e:
        #     # Don't suppress it here, let it propagate
        #     raise e

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer

    @extend_schema(**FORGOT_PASSWORD_SCHEMA)
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return api_response(status.HTTP_400_BAD_REQUEST, message="Email is required")

        if not User.objects.filter(email=email).exists():
            return api_response(status.HTTP_404_NOT_FOUND, message="User not found")

        user = User.objects.get(email=email)  # Safe because of exists() check

        # Create the PasswordResetRequest 
        PasswordResetRequestTokenGenerator.objects.create(user=user)

        return api_response(status.HTTP_200_OK, message="Password reset link sent to your email")
    

class UpdatePasswordView(APIView):
    @extend_schema(**UPDATE_PASSWORD_SCHEMA)
    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        if not uidb64 or not token or not password:
            return api_response(status.HTTP_400_BAD_REQUEST, message="All fields are required")

        # Decode the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        if not User.objects.filter(pk=uid).exists():
            return api_response(status.HTTP_400_BAD_REQUEST, message="Invalid user ID")

        user = User.objects.get(pk=uid)  # Safe because of `exists()` check
        if not default_token_generator.check_token(user, token):
            return api_response(status.HTTP_400_BAD_REQUEST, message="Invalid or expired token")

        user.set_password(password)
        user.is_active = True  # Optional: Activate the user if needed
        user.save()

        return api_response(status.HTTP_200_OK, message="Password updated successfully")
