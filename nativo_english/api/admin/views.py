# from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .serializer import AdminUserCreateSerializer
from nativo_english.api.shared.utils import api_response, api_exception_handler
from rest_framework import status
from .permissions import IsAdminUserRole

# Admin All will go here
class AdminUserCreateView(APIView):
    serializer_class = AdminUserCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    # Extending the schema for the swagger UI view
    @extend_schema(
        tags=['Admin'],
        summary="(Admin-only) Access, CRUD -> USER, Content, Lessons etc.",
        description="API for whole app, accessible by admin only."
    )
    def post(self, request, *args, **kwargs):
        '''
        Request Type: POST
        Body/DATA: User data
        First create user by initiating serializer instance 
        then if all seems ok , then commit the records by using serializer save
        '''
        try:

            serializer = self.serializer_class()
            
            if serializer.is_valid():
                user = serializer.save()
                return api_response(status.HTTP_201_CREATED, 'Admin user created successfully')
        
        except Exception as ex:
            return api_exception_handler(ex, None)
