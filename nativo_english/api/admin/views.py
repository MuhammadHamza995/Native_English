# api/admin/views.py
from nativo_english.api.shared import messages
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiRequest, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from nativo_english.api.shared.utils import api_response, api_exception_handler
from nativo_english.api.shared.course.views import get_all_courses, create_course, update_course, get_course_by_id
import json
from django.contrib.auth.hashers import make_password
from nativo_english.api.admin.serializer import AdminUserSerializer, CourseImageSerializer
from nativo_english.api.admin.models import CourseImage
from nativo_english.api.shared.course.models import Course
from nativo_english.api.admin.permissions import IsAdminUserRole
from rest_framework.parsers import MultiPartParser, FormParser
from nativo_english.api.shared.course.serializer import CourseSerializer

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

    @extend_schema(
        tags=['Admin'],
        summary="Get All users (Can be accessed by user with admin role only)",
        description="Lists all users (if filter is applied for role/suspend)",
        parameters=[
            OpenApiParameter(name="role", location=OpenApiParameter.QUERY, description="Role of the user to filter by (optional)", required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name="is_active", location=OpenApiParameter.QUERY, description="Filter by active status, true or false (optional)", required=False, type=OpenApiTypes.BOOL),
            OpenApiParameter(name="page", location=OpenApiParameter.QUERY, description="Get other pages data, pass the page number", required=False, type=OpenApiTypes.INT),
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

        except Exception as ex:
            return api_exception_handler(ex)

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
                return api_response(status.HTTP_201_CREATED,messages.USER_CREATED_SUCCESS_MESSAGE, response_serializer.data)
            
            return api_response(status.HTTP_400_BAD_REQUEST,  messages.BAD_REQUEST_ERROR_MESSAGE)
        except Exception as ex:
            return api_exception_handler(ex)
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retrieve User by ID (can only be accessed by Admin user role --> GET /api/admin/users/{id})
# 2. Update User by ID (can only be accessed by Admin user role --> PUT /api/admin/users/{id})
# -----------------------------------------
class AdminUserRetrieveUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    @extend_schema(
        tags=['Admin'],
        summary="Retrieve User by ID (Can be accessed by user with admin role only)",
        description="Retrieves a specific user by ID if provided.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID")],
    )
    def get(self, request, id, *args, **kwargs):
        try:
            if id is not None:
                user = get_object_or_404(User, id=id)
                serializer = AdminUserSerializer(user)
                response_data = serializer.data

                return api_response(status.HTTP_200_OK, messages.USER_RETRIEVED_SUCCESS_MESSAGE, response_data)
                
        except Exception as ex:
            return api_exception_handler(ex)

    @extend_schema(
        tags=['Admin'],
        summary="Update User by ID (Can be accessed by user with admin role only)",
        description="Updates the user by specific ID.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID")],
    )
    def put(self, request, id=None, *args, **kwargs):
        try:
            # Ensure the user exists
            user = get_object_or_404(User, id=id)
            serializer = self.serializer_class(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return api_response(status.HTTP_200_OK,messages.USER_UPDATED_SUCCESS_MESSAGE)
            return api_response(status.HTTP_400_BAD_REQUEST, serializer.errors)
        
        except Exception as ex:
            return api_exception_handler(ex)
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Update User Role by ID (can only be accessed by Admin user role --> PUT /api/admin/users/{id}/role)
# -----------------------------------------
class AdminUserRoleUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    @extend_schema(
        tags=['Admin'],
        summary="Update User Role (Can be accessed by user with admin role only)",
        description="Updates the role of the user by ID.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID")],
    )
    def put(self, request, id, *arg, **kwargs):
        try:
            # Ensure the user exists
            user = get_object_or_404(User, id=id)
            updated_role = request.data.get('role')

            if updated_role:
                user.role = updated_role
                user.save()
                response_serializer = self.serializer_class(user)

                return api_response(status.HTTP_200_OK, messages.USER_ROLE_UPDATED_SUCCESS_MESSAGE.format(id=id), response_serializer.data)
            else:
                return api_response(status.HTTP_400_BAD_REQUEST, f'''{messages.NO_USER_ROLE_PROVIDED}''')

        except Exception as ex:
            return api_exception_handler(ex, "Error updating user role.")


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
        description="Updates the isActive variable of the user to true or false (based on the action).",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="User ID"),
            OpenApiParameter("action", OpenApiTypes.STR, OpenApiParameter.PATH, required=True, description="Action to perform: 'activate' or 'suspend'"),
        ],
        request=OpenApiResponse(
            response=AdminUserSerializer,
            description="User status update request",
            examples=[{'username': 'john_doe', 'email': 'john@example.com'}],
        ),
    )
    def post(self, request, id=None, action=None, *arg, **kwargs):
        try:
            if action not in ['activate', 'suspend']:
                return api_response(status.HTTP_400_BAD_REQUEST, "Invalid action. Must be 'activate' or 'suspend'.")

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


        except Exception as ex:
            raise ex

        
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

    @extend_schema(
        tags=['Admin Course'],
        summary="Get All Courses (Admin access only)",
        description="Lists all courses with optional filters by title and is_paid.",
        parameters=[
            OpenApiParameter(
                name="title",
                location=OpenApiParameter.QUERY,
                description="Name of the course to filter by (optional)",
                required=False,
                type=OpenApiTypes.STR
            ),
            OpenApiParameter(
                name="is_paid",
                location=OpenApiParameter.QUERY,
                description="Filter by paid status, true or false (optional)",
                required=False,
                type=OpenApiTypes.BOOL
            ),
            OpenApiParameter(
                name="page",
                location=OpenApiParameter.QUERY,
                description="Page number to retrieve data from",
                required=False,
                type=OpenApiTypes.INT
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
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

        except Exception as ex:
            raise ex

    @extend_schema(
        tags=['Admin Course'],
        summary="Create a New Course (Admin access only)",
        description="Creates a new course by Admin User.",
    )
    def post(self, request, *args, **kwargs):
        try:
            result = create_course(request.data)

            if "error" in result or "non_field_errors" in result:
                return api_response(status.HTTP_400_BAD_REQUEST, "Error creating course", result)
            
            return api_response(status.HTTP_201_CREATED, 'Course created successfully', result)

        except Exception as ex:
            raise ex


        if "error" in result or "non_field_errors" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': messages.COURSE_CREATED_SUCCESS_MESSAGE, 'data': result}, status=status.HTTP_201_CREATED)
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

    @extend_schema(
        tags=['Admin Course'],
        summary="Retrieve Course by ID (Admin access only)",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="Course ID")
        ]
    )
    def get(self, request, id, *args, **kwargs):
        course_data = get_course_by_id(id)
        return api_response(status.HTTP_200_OK, messages.COURSE_RETRIEVED_SUCCESS_MESSAGE, course_data)

    @extend_schema(
        tags=['Admin Course'],
        summary="Update course by ID (Can be accessed by user with admin role only)",
        description="Updates the course by specific Id.",
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, required=True, description="Course ID")
        ],
    )
    def put(self, request, id=None, *args, **kwargs):
        try:
            result = update_course(id, request.data)

            # Check for validation or non-field errors
            if "error" in result or "non_field_errors" in result:
                return api_response(status.HTTP_400_BAD_REQUEST, 'Bad request: ' + str(result))

            return api_response(status.HTTP_200_OK, 'Course updated successfully', result)

        except Exception as ex:
            # Catch any exception and return it with an appropriate error response
            return api_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(ex))

        if "error" in result or "non_field_errors" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': messages.COURSE_UPDATED_MESSAGE, 'data': result}, status=status.HTTP_200_OK)
    


        # If an image file is provided, save it
        if image:
            # Assuming the CourseImage model has a field to store the image
            course_image = CourseImage(course=course, image=image)
            course_image.save()
            return Response(CourseImageSerializer(course_image).data, status=status.HTTP_201_CREATED)

        # If an image URL is provided, process it (you might want to save it to the model)
        if image_url:
            # Assuming the CourseImage model has a field to store the image URL
            course_image = CourseImage(course=course, image_url=image_url)
            course_image.save()
            return Response(CourseImageSerializer(course_image).data, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['Admin'],
    summary="Upload Course Image",
    description="Upload an image for a specific course.",
    responses={
        201: OpenApiResponse(
            description="Course image uploaded successfully",
            response=CourseImageSerializer
        ),
        400: OpenApiResponse(
            description="Bad request, invalid data"
        ),
    },
    parameters=[
        OpenApiParameter(
            name='course_id', 
            type=int, 
            location='path',  # Corrected to string 'path'
            required=True, 
            description='The ID of the course'
        ),
        OpenApiParameter(
            name='image', 
            type=OpenApiTypes.OBJECT, 
            location='form',  # Corrected to string 'form'
            required=True, 
            description='The image to upload'
        ),
    ]
)
class CourseImageUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        image = request.FILES.get('image')
        if not image:
            return Response({"detail": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)

        course.image = image
        course.save()

        serializer = CourseImageSerializer(course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
