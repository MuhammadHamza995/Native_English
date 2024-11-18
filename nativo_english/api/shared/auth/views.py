from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer
# from .serializers import LoginSerializer,
from rest_framework.response import Response
from django.contrib.auth import authenticate
from nativo_english.api.shared.utils import api_response, api_exception_handler

# Create your views here.

# RegisterView for Registration API
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# LoginView for Login API
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [permissions.AllowAny]

#     # POST API
#     def post (self, request, *args, **kwargs):
#         serializer = self.get_serializer(data = request.data)
#         serializer.is_valid(raise_exception = True)

#         user = serializer.validated_data['user']


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
     serializer = self.get_serializer(data=request.data)
 
    # The is_valid() method will raise a ValidationError if the data is invalid.
    # No need for try-except, as the middleware will handle the exception
     serializer.is_valid(raise_exception=True)
    
     return api_response(status.HTTP_200_OK, message='Login Successful', data=serializer.validated_data)

        

# This function will check for token present in Authorization header or not
def is_token_present_in_header(request):
    auth_header = request.headers.get('Authorization')
    
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]

    # If no token or invalid header, return None
    return None
