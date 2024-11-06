# api/admin/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiRequest, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .serializer import AdminUserSerializer
from nativo_english.api.shared.user.models import User
from .permissions import IsAdminUserRole
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from nativo_english.api.shared.utils import api_response, api_exception_handler
import json

# -----------------------------------------
class AdminUserPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum limit of items per page
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Users (can only be access by Admin user rol --> GET /api/admin/users/)
# 2. Create New User user request data (can only be access by Admin user rol --> POST /api/admin/users/{id})
# -----------------------------------------
class AdminUserListCreateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [
        IsAuthenticated, 
        IsAdminUserRole
    ]
    pagination_class = AdminUserPagination

    @extend_schema(
        tags=['Admin'],
        summary="Get All users (Can be accessed by user with admin role only)",
        description="Lists all users (if filter is applied for role/suspend)",
        parameters= [
            # Query parameters (optional)
            OpenApiParameter(
                name="role",
                location=OpenApiParameter.QUERY,
                description="Role of the user to filter by (optional)",
                required=False,
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name="is_active",
                location=OpenApiParameter.QUERY,
                description="Filter by active status, true or false (optional)",
                required=False,
                type=OpenApiTypes.BOOL
            ),
            OpenApiParameter(
                name="page",
                location=OpenApiParameter.QUERY,
                description="get other pages data, pass the page number",
                required=False,
                type=OpenApiTypes.INT
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            # Get query parameters for filtering
            role = request.query_params.get('role')
            is_active = request.query_params.get('is_active')

            # Get all users first
            queryset = User.objects.only("id", "username", "email", "first_name", "last_name", "is_active")
            
            if role:
                queryset = queryset.filter(role=role)

            if is_active is not None:
                is_active = is_active.lower() == 'true'
                queryset = queryset.filter(is_active = is_active)

            
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            serializer = self.serializer_class(page, many=True)
            
            if page is not None:
                # using custom response helper to structure the response
                response_data = {
                    "count": paginator.page.paginator.count,
                    "num_pages": paginator.page.paginator.num_pages,
                    "current_page": paginator.page.number,
                    "results": serializer.data,
                }
                return api_response(status.HTTP_200_OK, 'Users List Retrieved Successfully', response_data)

            serializer = self.serializer_class(queryset, many=True)
            
            return api_response(status.HTTP_200_OK, 'Users List Retrieved Successfully', serializer.data)

        except Exception as ex:
            raise ex

    @extend_schema(
        tags=['Admin'],
        summary="Creates a new User (Can be accessed by user with admin role only)",
        description="Creates a new user by Admin User.",
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                response_serializer = self.serializer_class(user)
                return api_response(status.HTTP_201_CREATED, 'User created successfully', response_serializer.data)
            return api_response(status.HTTP_400_BAD_REQUEST, 'BAD Request')
        except Exception as ex:
            raise ex
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retreive User by ID (can only be access by Admin user rol --> GET /api/admin/users/{id})
# 2. Update User by ID (can only be access by Admin user rol --> PUT /api/admin/users/{id})
# -----------------------------------------
class AdminUserRetrieveUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = PageNumberPagination


    @extend_schema(
        tags=['Admin'],
        summary="Retrieve User by ID (Can be accessed by user with admin role only)",
        description="Retrieves a specific user by ID if provided.",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID")
        ],
    )
    def get(self, request, id, *args, **kwargs):
        try:
        # Check if Id is present:
            if id is not None:
                # Retrieve user by ID from the URL
                user = get_object_or_404(User, id=id)

                # Serialize the user data
                serializer = AdminUserSerializer(user)

                response_data = serializer.data

                return api_response(status.HTTP_200_OK, 'User retrieved Successfully', response_data)
                
        except Exception as ex:
            raise ex

    
    @extend_schema(
        tags=['Admin'],
        summary="Update User by ID (Can be accessed by user with admin role only)",
        description="Updates the user by specific Id.",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID")
        ],
    )
    def put(self, request, id=None, *args, **kwargs):
        try:
            user = get_object_or_404(User, id=id)
            serializer = self.serializer_class(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return api_response(status.HTTP_200_OK,"User updated successfully")
            return api_response(status.HTTP_400_BAD_REQUEST, serializer.errors)
        
        except Exception as ex:
            raise ex
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Update User Role by ID (can only be access by Admin user rol --> PUT /api/admin/users/{id}/role)
# -----------------------------------------
class AdminUserRoleUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = PageNumberPagination

    @extend_schema(
        tags=['Admin'],
        summary="Update User Role (Can be accessed by user with admin role only)",
        description="Updates the role of the user by ID.",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID"),
        ],
        request=OpenApiResponse(
            response=AdminUserSerializer,
            description="User creation request",
            examples=[{'username': 'john_doe', 'email': 'john@example.com'}],
        ),
    )
    def put(self, request, id, *arg, **kwargs):
        try:
            user = get_object_or_404(User, id=id)
            updated_role = request.data.get('role')

            if updated_role:
                user.role = updated_role
                user.save()
                response_serializer = self.serializer_class(user)

                return api_response(status.HTTP_200_OK, f'''User role updated successfully for {id}''', response_serializer.data)
            else:
                return api_response(status.HTTP_400_BAD_REQUEST, f'''No User Role Provided''')
        except Exception as ex:
            raise ex

# -----------------------------------------
# This view corresponds to following endpoint
# 1. Update user isActive status to true(can only be access by Admin user rol --> PUT /api/admin/users/{id}/activate/)
# -----------------------------------------
class AdminUserActivateSuspendUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    @extend_schema(
        tags=['Admin'],
        summary="Update User Status (Can be accessed by user with admin role only)",
        description="Updates the isActive variable of the user to true.",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID"),
        ],
        request=OpenApiResponse(
            response=AdminUserSerializer,
            description="User creation request",
            examples=[{'username': 'john_doe', 'email': 'john@example.com'}],
        ),
    )
    def post(self, request, id = None, action = None, *arg, **kwargs):
        try:
            user = get_object_or_404(User, id=id)
            if action == "activate":
                user.is_active = True
                user.save()
                response_serializer = self.serializer_class(user)
                return api_response(status.HTTP_200_OK, f'''User activated successfully for {id}''', response_serializer.data)
            elif action == "suspend":
                user.is_active = False
                user.save()
                response_serializer = self.serializer_class(user)
                return api_response(status.HTTP_200_OK, f'''User suspended successfully for {id}''', response_serializer.data)

        except Exception as ex:
            raise ex
        

# -----------------------------------------
# This view corresponds to following endpoint
# 1. Update user isActive status to false(can only be access by Admin user rol --> PUT /api/admin/users/{id}/suspend/)
# -----------------------------------------
# class AdminUserSuspendUpdateView(APIView):
#     serializer_class = AdminUserSerializer
#     permission_classes = [IsAuthenticated, IsAdminUserRole]

#     @extend_schema(
#         tags=['Admin'],
#         summary="Update User Role (Can be accessed by user with admin role only)",
#         description="Updates the role of the user by ID.",
#         parameters=[
#             OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID"),
#         ],
#         request=OpenApiResponse(
#             response=AdminUserSerializer,
#             description="User creation request",
#             examples=[{'username': 'john_doe', 'email': 'john@example.com'}],
#         ),
#     )
#     def put(self, request, id, *arg, **kwargs):
#         try:
#             user = get_object_or_404(User, id=id)

#             if user.is_active:
#                 user.is_active = False
#                 response_serializer = self.serializer_class(user)

#                 return api_response(status.HTTP_200_OK, '''User status updated successfully for {id}''', response_serializer.data)
#         except Exception as ex:
#             raise ex