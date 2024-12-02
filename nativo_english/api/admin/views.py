# api/admin/views.py
from nativo_english.api.shared import messages

# api/admin/views.py
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiRequest, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from nativo_english.api.admin.models import Course,CourseSection,CourseLesson
from .serializer import AdminUserSerializer
from nativo_english.api.shared.course.serializer import CourseSerializer, CourseSectionSerializer, CourseLessonSerializer
from .serializer import AdminUserSerializer,UserSerializer
from nativo_english.api.shared.user.models import User
from .permissions import IsAdminUserRole
from django.shortcuts import get_object_or_404
from nativo_english.api.shared.utils import api_response, api_exception_handler
from rest_framework.exceptions import NotFound
from nativo_english.api.shared.course.views import get_all_courses, create_course, update_course, get_course_by_id, get_all_course_sections, get_course_section_by_id, update_course_section, create_course_section, create_course_lesson, get_all_course_lessons, get_course_lesson_by_id, update_course_lesson
from nativo_english.api.shared.utils import api_response, api_exception_handler
from rest_framework.exceptions import NotFound
import json
from django.contrib.auth.hashers import make_password
from .swagger_schema import GET_USER_LIST_SCHEMA, POST_USER_SCHEMA , GET_USER_BY_ID_SCHEMA , UPDATE_USER_BY_ID_SCHEMA, UPDATE_USER_ROLE_SCHEMA, UPDATE_USER_STATUS_SCHEMA, GET_ADMIN_COURSE_LIST_SCHEMA, POST_ADMIN_COURSE_CREATE_SCHEMA, GET_ADMIN_COURSE_RETRIEVE_SCHEMA, UPDATE_ADMIN_COURSE_UPDATE_SCHEMA, GET_ADMIN_COURSE_LESSON_RETRIEVE_SCHEMA, UPDATE_ADMIN_COURSE_LESSON_UPDATE_SCHEMA, GET_ADMIN_ALL_COURSE_LESSON_RETRIEVE_SCHEMA, POST_ADMIN_COURSE_LESSON_CREATE_SCHEMA, GET_ADMIN_COURSE_ALL_SECTION_SCHEMA, POST_ADMIN_COURSE_SECTION_CREATE_SCHEMA, GET_ADMIN_COURSE_SECTION_DETAIL_BY_ID_SCHEMA, UPDATE_ADMIN_COURSE_SECTION_BY_ID_SCHEMA

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
        
        if not queryset.exists():
            return api_response(status.HTTP_404_NOT_FOUND, messages.NO_USER_FOUND)

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
                
    @extend_schema(**UPDATE_USER_BY_ID_SCHEMA)
    def put(self, request, id=None, *args, **kwargs):
        # Ensure the user exists
        try:
            user = get_object_or_404(User, id=id)
        except Exception as e:
            return api_response(status.HTTP_404_NOT_FOUND, {"detail": "User not found."})

        # Update the user instance with partial data
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return api_response(
                    status.HTTP_200_OK,
                    {"status": 200, "message": "User updated successfully."}
                )
            except Exception as save_error:
                return api_response(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    {"detail": str(save_error)}
                )

        return api_response(
            status.HTTP_400_BAD_REQUEST,
            {"errors": serializer.errors}
        )
 
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

            return api_response(status.HTTP_200_OK, messages.USER_ROLE_UPDATED_SUCCESS_MESSAGE.format(id=id), response_serializer.data)
        else:
            return api_response(status.HTTP_400_BAD_REQUEST, f'''{messages.NO_USER_ROLE_PROVIDED}''')



# -----------------------------------------
# This view corresponds to following endpoint
# 1. Update user isActive status to true(can only be access by Admin user rol --> PUT /api/admin/users/{id}/activate/)
# -----------------------------------------
class AdminUserActivateSuspendUpdateView(APIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    @extend_schema(**UPDATE_USER_STATUS_SCHEMA)  # Use the corrected schema
    def post(self, request, id=None, action=None, *arg, **kwargs):
        # action = kwargs.get('action')
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
        serializer = CourseSerializer(data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the course and return success response
            course = serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': messages.COURSE_CREATED_SUCCESS_MESSAGE,
                'data': CourseSerializer(course).data
            }, status=status.HTTP_201_CREATED)
        
        # Return error response if the serializer is invalid
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': messages.INVALID_DATA_MESSAGE,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
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
    # Check if the ID parameter is provided
     if not id:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': messages.ID_REQUIRED_MESSAGE,
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Try to retrieve the course by ID
     try:
        course = Course.objects.get(id=id)
     except Course.DoesNotExist:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': messages.COURSE_NOT_FOUND_MESSAGE,
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Serialize and validate input data
     serializer = CourseSerializer(course, data=request.data, partial=True)
     if serializer.is_valid():
        # Save the updated course
        updated_course = serializer.save()
        return Response({
            'status': status.HTTP_200_OK,
            'message': messages.COURSE_UPDATED_SUCCESS_MESSAGE,
            'data': CourseSerializer(updated_course).data,
        }, status=status.HTTP_200_OK)

    # Handle validation errors for specific fields
     error_details = serializer.errors

    # Title validation error
     if 'title' in error_details:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': messages.TITLE_REQUIRED_MESSAGE,
            'errors': error_details['title'],
        }, status=status.HTTP_400_BAD_REQUEST)

    # Description validation error
     if 'description' in error_details:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': messages.DESCRIPTION_REQUIRED_MESSAGE,
            'errors': error_details['description'],
        }, status=status.HTTP_400_BAD_REQUEST)

    # Handle errors for other fields dynamically
     field_errors = {
        field: {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': messages.INVALID_FIELD_MESSAGE.format(field=field),
            'errors': error,
        }
        for field, error in error_details.items()
        if field not in ['title', 'description']
     }

     if field_errors:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': messages.INVALID_FIELDS_MESSAGE,
            'errors': field_errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    # If no specific field errors are matched, return a general error
     return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': messages.INVALID_DATA_MESSAGE,
        'errors': error_details,
     }, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------

# -----------------------------------------

# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Courses Section(can only be access by Admin user rol --> GET /api/admin/course/section)
# 2. Create New Course Section user request data (can only be access by Admin user rol --> POST /api/admin/course/section)
# -----------------------------------------
class AdminCourseSectionListCreateView(APIView):
    serializer_class = CourseSectionSerializer
    permission_classes = [
        IsAuthenticated, 
        IsAdminUserRole
    ]
    pagination_class = AdminUserPagination

    @extend_schema(**GET_ADMIN_COURSE_ALL_SECTION_SCHEMA)
    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        course_id = request.query_params.get('course_id')

        sections = get_all_course_sections(filter_title=title, course_id=course_id)

        if not sections:
            return api_response(status.HTTP_404_NOT_FOUND,messages.SECTION_NOT_FOUND_MESSAGE)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(sections, request)

        if page is not None:
            response_data = {
                "count": paginator.page.paginator.count,
                "num_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "results": page,
            }
            return api_response(status.HTTP_200_OK, messages.SECTION_LIST_RETRIEVED_SUCCESS_MESSAGE, response_data)

        return api_response(status.HTTP_200_OK, messages.SECTION_LIST_RETRIEVED_SUCCESS_MESSAGE, sections)

  
class AdminCourseSectionCreateView(APIView):
     @extend_schema(**POST_ADMIN_COURSE_SECTION_CREATE_SCHEMA)
     def post(self, request, *args, **kwargs):
        # Attempt to create the course section
        result = create_course_section(request.data)

        # Handle error response
        if isinstance(result, dict) and 'errors' in result:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                messages.SECTION_CREATION_ERROR_MESSAGE,
                {'errors': result['errors']}
            )

        # Return success response
        return api_response(
            status.HTTP_201_CREATED,
            messages.COURSE_SECTION_CREATED_SUCCESS_MESSAGE,
            result
        )

# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retreive Course Section by ID (can only be access by Admin user rol --> GET /api/admin/course/section/{id})
# 2. Update Course Section by ID (can only be access by Admin user rol --> PUT /api/admin/course/section/{id})
# -----------------------------------------
class AdminCourseSectionRetrieveUpdateView(APIView):
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = PageNumberPagination

    @extend_schema(**GET_ADMIN_COURSE_SECTION_DETAIL_BY_ID_SCHEMA)
    def get(self, request, course_section_id,*args, **kwargs):
        course_data = get_course_section_by_id(course_section_id)
        return api_response(status.HTTP_200_OK, messages.COURSE_SECTION_RETRIEVED_SUCCESS_MESSAGE, course_data)

    @extend_schema(**UPDATE_ADMIN_COURSE_SECTION_BY_ID_SCHEMA)
    def put(self, request, course_section_id=None, *args, **kwargs):
    # Ensure course_section_id is provided and valid
     if not course_section_id:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Course Section ID is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve the course section by ID
     try:
        course_section = CourseSection.objects.get(id=course_section_id)
     except CourseSection.DoesNotExist:
        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Course section with the given ID does not exist.'
        }, status=status.HTTP_404_NOT_FOUND)

    # Serialize the data and validate it
     serializer = CourseSectionSerializer(course_section, data=request.data, partial=True)

    # If serializer is valid, update and save the course section
     if serializer.is_valid():
        updated_course_section = serializer.save()
        return Response({
            'status': status.HTTP_200_OK,
            'message': messages.COURSE_SECTION_UPDATED_SUCCESS_MESSAGE,
            'data': CourseSectionSerializer(updated_course_section).data,
        }, status=status.HTTP_200_OK)
    
    # If serializer is invalid, return validation errors
     return Response({
        'status': status.HTTP_400_BAD_REQUEST,
        'message': 'Validation Error',
        'errors': serializer.errors,
     }, status=status.HTTP_400_BAD_REQUEST)
# -----------------------------------------

# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Courses Lesson(can only be access by Admin user rol --> GET /api/admin/course/section/lesson)
# 2. Create New Course Lesson user request data (can only be access by Admin user rol --> POST /api/admin/course/section/lesson)
# -----------------------------------------

class AdminCourseLessonListCreateView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [
        IsAuthenticated, 
        IsAdminUserRole
    ]
    pagination_class = AdminUserPagination

    @extend_schema(**GET_ADMIN_ALL_COURSE_LESSON_RETRIEVE_SCHEMA)
    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title')
        course_id = request.query_params.get('course_id')
        section_id = request.query_params.get('section_id')
        # course_id = int(course_id) if course_id else None
        # section_id = int(section_id) if section_id else None
        print(course_id, section_id)

        lessons = get_all_course_lessons(filter_title=title, course_id=course_id, section_id=section_id)

        if not lessons:
            return api_response(status.HTTP_404_NOT_FOUND,messages.LESSON_NOT_FOUND_MESSAGE)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(lessons, request)

        if page is not None:
            response_data = {
                "count": paginator.page.paginator.count,
                "num_pages": paginator.page.paginator.num_pages,
                "current_page": paginator.page.number,
                "results": page,
            }
            return api_response(status.HTTP_200_OK, messages.LESSON_LIST_RETRIEVED_SUCCESS_MESSAGE, response_data)

        return api_response(status.HTTP_200_OK, messages.LESSON_LIST_RETRIEVED_SUCCESS_MESSAGE, lessons)

    @extend_schema(**POST_ADMIN_COURSE_LESSON_CREATE_SCHEMA)

    def post(self, request, *args, **kwargs):
        result = create_course_lesson(request.data)

        if isinstance(result, dict):
            if 'errors' in result:
                return api_response(status.HTTP_400_BAD_REQUEST, messages.LESSON_CREATION_ERROR_MESSAGE, result['errors'])
        
        return api_response(status.HTTP_201_CREATED, messages.COURSE_LESSON_CREATED_SUCCESS_MESSAGE, result)
# -----------------------------------------

# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retreive Course Lesson by ID (can only be access by Admin user rol --> GET /api/admin/course/section/lesson/{id})
# 2. Update Course Lesson by ID (can only be access by Admin user rol --> PUT /api/admin/course/section/lesson/{id})
# -----------------------------------------
class AdminCourseLessonRetrieveUpdateView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = PageNumberPagination

    @extend_schema(**GET_ADMIN_COURSE_LESSON_RETRIEVE_SCHEMA)
    def get(self, request, course_lesson_id,*args, **kwargs):
        course_data = get_course_lesson_by_id(course_lesson_id)
        return api_response(status.HTTP_200_OK, messages.COURSE_LESSON_RETRIEVED_SUCCESS_MESSAGE, course_data)


    @extend_schema(**UPDATE_ADMIN_COURSE_LESSON_UPDATE_SCHEMA)
    def put(self, request, course_lesson_id=None, *args, **kwargs):
     try:
        # Check if the course lesson exists
        course_lesson = CourseLesson.objects.get(id=course_lesson_id)  # Assuming CourseLesson is the model
     except CourseLesson.DoesNotExist:
        return api_response(status.HTTP_404_NOT_FOUND, "Course lesson not found.")
    
    # If course lesson exists, proceed to validation
     serializer = CourseLessonSerializer(course_lesson, data=request.data, partial=True)

     if serializer.is_valid():
        # Perform the update operation if data is valid
        result = update_course_lesson(course_lesson_id, request.data)

        # Handle validation or update errors
        if "error" in result or "non_field_errors" in result:
            return api_response(
                status.HTTP_400_BAD_REQUEST,
                messages.BAD_REQUEST_ERROR_MESSAGE,
                result
            )
        
        # Return a successful response
        return api_response(
            status.HTTP_200_OK,
            messages.COURSE_LESSON_UPDATED_SUCCESS_MESSAGE,
            result
        )

    # Handle validation errors and return them in the response
     error_details = serializer.errors

    # Checking specific errors related to the parameters
     if 'course' in error_details:
        return api_response(status.HTTP_400_BAD_REQUEST, messages.INVALID_COURSE_PARAMETER_MESSAGE, error_details['course'])
    
     if 'title' in error_details:
        return api_response(status.HTTP_400_BAD_REQUEST,messages.TITLE_REQUIRED_MESSAGE, error_details['title'])
    
     if 'description' in error_details:
        return api_response(status.HTTP_400_BAD_REQUEST, messages.DESCRIPTION_REQUIRED_MESSAGE, error_details['description'])

    # If any error occurs, return general validation error
     return api_response(
        status.HTTP_400_BAD_REQUEST,
        messages.VALIDATION_ERROR_MESSAGE ,
        error_details
     )
# -----------------------------------------
