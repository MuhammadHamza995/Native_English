# api/admin/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import AdminUserSerializer
from nativo_english.api.shared.user.models import User
from .permissions import IsAdminUserRole
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from nativo_english.api.shared.utils import api_response, api_exception_handler

class AdminUserPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum limit of items per page


class AdminUserListCreateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [
        IsAuthenticated, 
        IsAdminUserRole
    ]
    pagination_class = AdminUserPagination

    @extend_schema(
        tags=['Admin'],
        summary="(Admin-only) List Users",
        description="Lists all users",
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = User.objects.only("id", "username", "email", "first_name", "last_name")
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = self.serializer_class(queryset, many=True)
            response_data =  paginator.get_paginated_response(serializer.data)

            return api_response(status.HTTP_200_OK, 'Users List Retrieved Successfully', response_data)

        except Exception as ex:
            raise ex

    @extend_schema(
        tags=['Admin'],
        summary="(Admin-only) Create a new user",
        description="Creates a new user.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Admin user created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdminUserRetrieveUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = PageNumberPagination


    @extend_schema(
        tags=['Admin'],
        summary="(Admin-only) List Users or Retrieve User by ID",
        description="Lists all users if no ID is provided; retrieves a specific user by ID if provided.",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID")
        ],
    )
    def get(self, request, id, *args, **kwargs):
        # Check if Authorization header contains a Bearer token
        auth_header = request.headers.get("Authorization", "")
        print(auth_header)
        return Response({"message": "User created"})
    
    @extend_schema(
        tags=['Admin'],
        summary="(Admin-only) Update User by ID",
        description="Updates the user by ID.",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID")
        ],
    )
    def put(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(User, id=id)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
