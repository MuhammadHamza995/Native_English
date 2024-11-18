# api/admin/views.py
from nativo_english.api.shared import messages

# api/admin/views.py
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiRequest, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializer import AdminUserSerializer #,UserSerializer
from nativo_english.api.shared.course.serializer import CourseSerializer
from nativo_english.api.shared.user.models import User
from .permissions import IsAdminUserRole
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from nativo_english.api.shared.utils import api_response
from nativo_english.api.shared.course.views import get_all_courses, create_course, update_course, get_course_by_id
import json
from django.contrib.auth.hashers import make_password
from .swagger_schema import GET_USER_LIST_SCHEMA, POST_USER_SCHEMA , GET_USER_BY_ID_SCHEMA , UPDATE_USER_BY_ID_SCHEMA, UPDATE_USER_ROLE_SCHEMA, UPDATE_USER_STATUS_SCHEMA, GET_ADMIN_COURSE_LIST_SCHEMA, POST_ADMIN_COURSE_CREATE_SCHEMA, GET_ADMIN_COURSE_RETRIEVE_SCHEMA, UPDATE_ADMIN_COURSE_UPDATE_SCHEMA


# -----------------------------------------
class AdminUserPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum limit of items per page
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Users (can only be accessed by Admin user role --> GET /api/admin/users/)
# 2. Create New User (can only be accessed by Admin user role --> POST /api/admin/users/)
# -----------------------------------------
class AdminUserListCreateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = AdminUserPagination

    # ------------------------------------
    @extend_schema(**GET_USER_LIST_SCHEMA)
    def get(self, request, *args, **kwargs):
        '''
            GET USER LIST METHOD
            GET /api/admin/users/ (Get all users with some filter, and can only be accessible by Admin role)  
        '''
        # Get query parameters for filtering
        role = request.query_params.get('role')
        is_active = request.query_params.get('is_active')

        # Get all users first
        queryset = User.objects.only("id", "username", "email", "first_name", "last_name", "is_active")
        
        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)

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
            return api_response(status.HTTP_200_OK, messages.USERS_LIST_RETRIEVED_SUCCESS_MESSAGE, response_data)

        serializer = self.serializer_class(queryset, many=True)
        
        return api_response(status.HTTP_200_OK, messages.USERS_LIST_RETRIEVED_SUCCESS_MESSAGE, serializer.data)
        
    # ------------------------------------
    

    # ------------------------------------
    # POST USER LIST METHOD
    # POST /api/admin/users/ (Create new user, and can only be accessible by Admin role)
    # ------------------------------------
    

    @extend_schema(**POST_USER_SCHEMA)  # Extending the schema with the updated schema
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_serializer = self.serializer_class(user)
            return api_response(status.HTTP_201_CREATED, messages.USER_CREATED_SUCCESS_MESSAGE, response_serializer.data)

        return api_response(status.HTTP_400_BAD_REQUEST, messages.BAD_REQUEST_ERROR_MESSAGE)
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retrieve User by ID (can only be accessed by Admin user role --> GET /api/admin/users/{id})
# 2. Update User by ID (can only be accessed by Admin user role --> PUT /api/admin/users/{id})
# -----------------------------------------
class AdminUserRetrieveUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    @extend_schema(**GET_USER_BY_ID_SCHEMA)
    def get(self, request, id, *args, **kwargs):
        if id is not None:
            user = get_object_or_404(User, id=id)
            serializer = AdminUserSerializer(user)
            response_data = serializer.data

            return api_response(status.HTTP_200_OK, messages.USER_RETRIEVED_SUCCESS_MESSAGE, response_data)
                
    @extend_schema(**UPDATE_USER_BY_ID_SCHEMA)  # Extending the schema with the updated schema
    def put(self, request, id=None, *args, **kwargs):
        # Ensure the user exists
        user = get_object_or_404(User, id=id)
        
        # Update the user instance with partial data
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return api_response(status.HTTP_200_OK, messages.USER_UPDATED_SUCCESS_MESSAGE)

        return api_response(status.HTTP_400_BAD_REQUEST, serializer.errors)
 
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Update User Role by ID (can only be accessed by Admin user role --> PUT /api/admin/users/{id}/role)
# -----------------------------------------

class AdminUserRoleUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]  # Custom permission

    @extend_schema(**UPDATE_USER_ROLE_SCHEMA)  # Use the schema defined in the schema file
    def put(self, request, id, *arg, **kwargs):
        # Ensure the user exists
        user = get_object_or_404(User, id=id)
        updated_role = request.data.get('role')

        if updated_role:
            user.role = updated_role
            user.save()

            # Serialize response
            response_serializer = self.serializer_class(user)

            return Response(
                {
                    'status': 200,
                    'message': f"{messages.USER_ROLE_UPDATED_SUCCESS_MESSAGE } for ID: {id}",
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {'status': 400, 'message': messages.NO_USER_ROLE_PROVIDED},
            status=status.HTTP_400_BAD_REQUEST
        )



# -----------------------------------------
# This view corresponds to following endpoint
# 1. Update user isActive status to true(can only be access by Admin user rol --> PUT /api/admin/users/{id}/activate/)
# -----------------------------------------
class AdminUserActivateSuspendUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    @extend_schema(**UPDATE_USER_STATUS_SCHEMA)  # Use the corrected schema
    def post(self, request, id=None, action=None, *arg, **kwargs):
        if action not in ['activate', 'suspend']:
            return api_response(status.HTTP_400_BAD_REQUEST, messages.INVALID_ACTION_MESSAGE)

        user = get_object_or_404(User, id=id)
        
        # Update user status based on the action
        if action == "activate":
            user.is_active = True
            user.save()
            response_serializer = self.serializer_class(user)
            
            return api_response(status.HTTP_200_OK, f'{messages.USER_UPDATED_SUCCESS_MESSAGE} for {id}', response_serializer.data)

        elif action == "suspend":
            user.is_active = False
            user.save()
            response_serializer = self.serializer_class(user)
            return api_response(status.HTTP_200_OK, f'{messages.USER_SUSPENDED_SUCCESS_MESSAGE} for {id}', response_serializer.data)

        
# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Courses (can only be access by Admin user rol --> GET /api/admin/course/)
# 2. Create New Course user request data (can only be access by Admin user rol --> POST /api/admin/course)
# -----------------------------------------
class AdminCourseListCreateView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticated, 
        IsAdminUserRole
    ]
    pagination_class = AdminUserPagination

    @extend_schema(**GET_ADMIN_COURSE_LIST_SCHEMA)

    def get(self, request, *args, **kwargs):
        # Retrieve query parameters for filtering
        title = request.query_params.get('title')
        is_paid = request.query_params.get('is_paid')

        queryset = get_all_courses(filter_title=title, filter_is_paid=is_paid)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = self.serializer_class(page, many=True)
        
        if not queryset:
            return api_response(status.HTTP_404_NOT_FOUND, messages.COURSE_NOT_FOUND_MESSAGE, serializer.data)
        
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            response_data = {
                "count": paginator.page.paginator.count,
                "num_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "results": serializer.data,
            }
            return api_response(status.HTTP_200_OK, messages.COURSE_LIST_RETRIEVED_SUCCESS_MESSAGE, response_data)

        serializer = self.serializer_class(queryset, many=True)
        
        return api_response(status.HTTP_200_OK, messages.COURSE_LIST_RETRIEVED_SUCCESS_MESSAGE, serializer.data)


    @extend_schema(**POST_ADMIN_COURSE_CREATE_SCHEMA)
    def post(self, request, *args, **kwargs):
    # Create the course using provided data
      result = create_course(request.data)

    # Check for errors in the result
      if "error" in result or "non_field_errors" in result:
        return api_response(status.HTTP_400_BAD_REQUEST, messages.COURSE_CREATE_ERROR_MESSAGE, result)
    
    # Return success message
      return api_response(status.HTTP_201_CREATED, messages.COURSE_CREATED_SUCCESS_MESSAGE, result)

# -----------------------------------------

# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retreive Course by ID (can only be access by Admin user rol --> GET /api/admin/course/{id})
# 2. Update Course by ID (can only be access by Admin user rol --> PUT /api/admin/course/{id})
# -----------------------------------------
class AdminCourseRetrieveUpdateView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = PageNumberPagination

    @extend_schema(**GET_ADMIN_COURSE_RETRIEVE_SCHEMA)
    def get(self, request, id, *args, **kwargs):
        course_data = get_course_by_id(id)
        return api_response(status.HTTP_200_OK, messages.COURSE_RETRIEVED_SUCCESS_MESSAGE, course_data)

    @extend_schema(**UPDATE_ADMIN_COURSE_UPDATE_SCHEMA)
    def put(self, request, id=None, *args, **kwargs):
    # Update the course using provided ID and data
     result = update_course(id, request.data)

    # Check for validation or non-field errors
     if "error" in result or "non_field_errors" in result:
        return api_response(status.HTTP_400_BAD_REQUEST, messages.BAD_REQUEST_ERROR_MESSAGE + str(result))

    # Return success message
     return api_response(status.HTTP_200_OK, messages.COURSE_UPDATED_MESSAGE, result)

# -----------------------------------------


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
