from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from nativo_english.api.shared.utils import api_response
from nativo_english.api.shared import messages
from drf_spectacular.utils import extend_schema
from .permissions import IsTeacherUserRole
from nativo_english.api.shared.course.serializer import (
    CourseSerializer, CourseSectionSerializer,
    CourseLessonSerializer )
from nativo_english.api.shared.course.views import (
    get_all_courses_with_pagination, create_course,
    get_course_detail_by_id, update_course,
    get_all_course_sections, create_course_section,
    get_course_section_by_id, update_course_section,
    get_all_course_lessons, create_course_lesson,
    get_course_lesson_by_id, update_course_lesson)

from .swagger_schema import (
    GET_TEACHER_COURSE_LIST_SCHEMA, POST_TEACHER_COURSE_CREATE_SCHEMA, 
    GET_TEACHER_COURSE_RETRIEVE_SCHEMA, UPDATE_TEACHER_COURSE_UPDATE_SCHEMA,
    GET_TEACHER_COURSE_ALL_SECTION_SCHEMA, POST_TEACHER_COURSE_SECTION_CREATE_SCHEMA,
    GET_TEACHER_COURSE_SECTION_DETAIL_BY_ID_SCHEMA, UPDATE_TEACHER_COURSE_SECTION_BY_ID_SCHEMA,
    GET_TEACHER_ALL_COURSE_LESSON_RETRIEVE_SCHEMA, GET_TEACHER_COURSE_LESSON_RETRIEVE_SCHEMA,
    POST_TEACHER_COURSE_LESSON_CREATE_SCHEMA, UPDATE_TEACHER_COURSE_LESSON_UPDATE_SCHEMA)


# Create your views here.
# -----------------------------------------
class TeacherUserPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Maximum limit of items per page
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Courses (can only be access by Teacher user rol --> GET /api/teacher/course/)
# 2. Create New Course user request data (can only be access by Teacher user rol --> POST /api/teacher/course)
# -----------------------------------------
class TeacherCourseListCreateView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticated, 
        IsTeacherUserRole
    ]

    @extend_schema(**GET_TEACHER_COURSE_LIST_SCHEMA)
    def get(self, request, *args, **kwargs):
        page_num = int(request.query_params.get('page_num', 1))
        page_size = int(request.query_params.get('page_size', 10))
        filter_title = request.query_params.get('title', None)
        filter_mode = request.query_params.get('mode', None)
        filter_is_paid = request.query_params.get('is_paid', None)
        filter_is_active = request.query_params.get('is_active', True)
        search_query = request.query_params.get('search', None)
        sort_field = request.query_params.get('sort_by', None)
        sort_order = request.query_params.get('sort_order', None)
        filter_level = request.query_params.get('level', None)

        owner_id = request.user.id
        queryset = get_all_courses_with_pagination(page_num, 
                                                   page_size, 
                                                   filter_title, 
                                                   filter_mode, 
                                                   filter_is_paid, 
                                                   filter_is_active, 
                                                   search_query, 
                                                   sort_field, 
                                                   sort_order,
                                                   owner_id,
                                                   filter_level)

        return api_response(status.HTTP_200_OK, messages.COURSE_LIST_RETRIEVED_SUCCESS_MESSAGE, queryset)


    @extend_schema(**POST_TEACHER_COURSE_CREATE_SCHEMA)
    def post(self, request, *args, **kwargs):
        request.data['owner'] = request.user.id
        
        # Create the course using provided data
        result = create_course(request)
        
        # Check for errors in the result
        if "error" in result or "non_field_errors" in result:
            return api_response(status.HTTP_400_BAD_REQUEST, messages.COURSE_CREATE_ERROR_MESSAGE, result)

        if any(
            isinstance(errors, list) and any("required" in getattr(err, "code", "") for err in errors)
            for errors in result.values()):
            return api_response(status.HTTP_400_BAD_REQUEST, messages.COURSE_CREATE_ERROR_MESSAGE, result)
        
        # Return success message
        return api_response(status.HTTP_201_CREATED, messages.COURSE_CREATED_SUCCESS_MESSAGE, result)

# -----------------------------------------

# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retreive Course by ID (can only be access by Teacher user rol --> GET /api/teacher/course/{id})
# 2. Update Course by ID (can only be access by Teacher user rol --> PUT /api/teacher/course/{id})
# -----------------------------------------
class TeacherCourseRetrieveUpdateView(APIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacherUserRole]
    pagination_class = TeacherUserPagination

    @extend_schema(**GET_TEACHER_COURSE_RETRIEVE_SCHEMA)
    def get(self, request, id, *args, **kwargs):
        course_data = get_course_detail_by_id(id, request.user.id)
        
        # Check if there is no course access to this teacher
        if not len(course_data):
            return api_response(status.HTTP_403_FORBIDDEN, messages.COURSE_NOT_FOUND_MESSAGE)
        
        return api_response(status.HTTP_200_OK, messages.COURSE_RETRIEVED_SUCCESS_MESSAGE, course_data)

    @extend_schema(**UPDATE_TEACHER_COURSE_UPDATE_SCHEMA)
    def put(self, request, id=None, *args, **kwargs):
        # Check for teacher accessing or updating the owner of his own course
        if request.data.get('owner') and request.data.get('owner') != request.user.id:
            return api_response(status.HTTP_403_FORBIDDEN, messages.COURSE_CANNOT_REASSIGN_BY_USER)
        
        # Update the course using provided ID and data
        result = update_course(id, request, request.user.id)

        # Check for validation or non-field errors
        if "error" in result or "non_field_errors" in result:
            return api_response(status.HTTP_400_BAD_REQUEST, messages.BAD_REQUEST_ERROR_MESSAGE + str(result))

        # Return success message
        return api_response(status.HTTP_200_OK, messages.COURSE_UPDATED_SUCCESS_MESSAGE, result)
# -----------------------------------------



# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Courses Section(can only be access by Teacher user rol --> GET /api/teacher/course/section)
# 2. Create New Course Section user request data (can only be access by Teacher user rol --> POST /api/teacher/course/section)
# -----------------------------------------
class TeacherCourseSectionListCreateView(APIView):
    serializer_class = CourseSectionSerializer
    permission_classes = [
        IsAuthenticated, 
        IsTeacherUserRole
    ]
    pagination_class = TeacherUserPagination

    @extend_schema(**GET_TEACHER_COURSE_ALL_SECTION_SCHEMA)
    def get(self, request, course_id, *args, **kwargs):
        title = request.query_params.get('title')

        course_data = get_course_detail_by_id(course_id, request.user.id)
        
        # Check if there is no course access to this teacher
        if not len(course_data):
            return api_response(status.HTTP_403_FORBIDDEN, messages.COURSE_NOT_FOUND_MESSAGE)
        
        sections = get_all_course_sections(request, course_id=course_id, filter_title=title)

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


    @extend_schema(**POST_TEACHER_COURSE_SECTION_CREATE_SCHEMA)
    def post(self, request, course_id, *args, **kwargs):

        if course_id is None or not len(get_course_detail_by_id(course_id, request.user.id)):
            return api_response(status.HTTP_400_BAD_REQUEST, messages.COURSE_NOT_FOUND_MESSAGE)
        
        request.data['fk_course_id'] = course_id

        result = create_course_section(request)
        if isinstance(result, dict):
            if 'errors' in result:
                return api_response(status.HTTP_400_BAD_REQUEST, messages.SECTION_CREATION_ERROR_MESSAGE, result['errors'])
            
            if any(
                isinstance(errors, list) and any("required" in getattr(err, "code", "") for err in errors)
                for errors in result.values()):
                return api_response(status.HTTP_400_BAD_REQUEST, messages.SECTION_CREATION_ERROR_MESSAGE, result)
        
        return api_response(status.HTTP_201_CREATED, messages.COURSE_SECTION_CREATED_SUCCESS_MESSAGE, result)
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retreive Course Section by ID (can only be access by Teacher user rol --> GET /api/teacher/course/section/{id})
# 2. Update Course Section by ID (can only be access by Teacher user rol --> PUT /api/teacher/course/section/{id})
# -----------------------------------------
class TeacherCourseSectionRetrieveUpdateView(APIView):
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticated, IsTeacherUserRole]
    pagination_class = TeacherUserPagination

    @extend_schema(**GET_TEACHER_COURSE_SECTION_DETAIL_BY_ID_SCHEMA)
    def get(self, request, course_id, course_section_id,*args, **kwargs):
        course_data = get_course_section_by_id(request, course_section_id, course_id)
        return api_response(status.HTTP_200_OK, messages.COURSE_SECTION_RETRIEVED_SUCCESS_MESSAGE, course_data)

    @extend_schema(**UPDATE_TEACHER_COURSE_SECTION_BY_ID_SCHEMA)
    def put(self, request, course_id, course_section_id, *args, **kwargs):
        if course_id is None:
            return api_response(status.HTTP_400_BAD_REQUEST, messages.COURSE_NOT_FOUND_MESSAGE)
        
        elif course_section_id is None:
            return api_response(status.HTTP_400_BAD_REQUEST, messages.COURSE_SECTION_NOT_FOUND_MESSAGE)
        
        request.data['fk_course_id'] = course_id
        result = update_course_section(request, course_section_id, course_id)

        if "error" in result or "non_field_errors" in result:
            return api_response(status.HTTP_400_BAD_REQUEST, messages.BAD_REQUEST_ERROR_MESSAGE, result)
        
        return api_response(status.HTTP_200_OK, messages.COURSE_SECTION_UPDATED_SUCCESS_MESSAGE, result)
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Get all Courses Lesson(can only be access by Teacher user rol --> GET /api/teacher/course/section/lesson)
# 2. Create New Course Lesson user request data (can only be access by Teacher user rol --> POST /api/teacher/course/section/lesson)
# -----------------------------------------
class TeacherCourseLessonListCreateView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAuthenticated, IsTeacherUserRole]
    pagination_class = TeacherUserPagination

    @extend_schema(**GET_TEACHER_ALL_COURSE_LESSON_RETRIEVE_SCHEMA)
    def get(self, request, course_section_id, *args, **kwargs):
        title = request.query_params.get('title')
        
        lessons = get_all_course_lessons(filter_title=title, section_id=course_section_id)

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

    @extend_schema(**POST_TEACHER_COURSE_LESSON_CREATE_SCHEMA)

    def post(self, request, course_section_id, *args, **kwargs):
        request.data['fk_section_id'] = course_section_id
        result = create_course_lesson(request.data)

        if isinstance(result, dict):
            if 'errors' in result:
                return api_response(status.HTTP_400_BAD_REQUEST, messages.LESSON_CREATION_ERROR_MESSAGE, result['errors'])
            if any("required" in err.code for errors in result.values() for err in errors):
                return api_response(status.HTTP_400_BAD_REQUEST, messages.LESSON_CREATION_ERROR_MESSAGE, result)
            
        return api_response(status.HTTP_201_CREATED, messages.COURSE_LESSON_CREATED_SUCCESS_MESSAGE, result)
# -----------------------------------------


# -----------------------------------------
# This view corresponds to following endpoints
# 1. Retreive Course Lesson by ID (can only be access by Admin user rol --> GET /api/admin/course/section/lesson/{id})
# 2. Update Course Lesson by ID (can only be access by Admin user rol --> PUT /api/admin/course/section/lesson/{id})
# -----------------------------------------
class TeacherCourseLessonRetrieveUpdateView(APIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAuthenticated, IsTeacherUserRole]
    pagination_class = TeacherUserPagination

    @extend_schema(**GET_TEACHER_COURSE_LESSON_RETRIEVE_SCHEMA)
    def get(self, request, course_section_id, course_lesson_id, *args, **kwargs):
        course_data = get_course_lesson_by_id(course_lesson_id)
        return api_response(status.HTTP_200_OK, messages.COURSE_LESSON_RETRIEVED_SUCCESS_MESSAGE, course_data)


    @extend_schema(**UPDATE_TEACHER_COURSE_LESSON_UPDATE_SCHEMA)
    def put(self, request, course_section_id, course_lesson_id=None, *args, **kwargs):
        request.data['fk_section_id'] = course_section_id
        result = update_course_lesson(course_lesson_id, request.data)

        if "error" in result or "non_field_errors" in result:
            return api_response(status.HTTP_400_BAD_REQUEST, messages.BAD_REQUEST_ERROR_MESSAGE, result)
        
        return api_response(status.HTTP_200_OK, messages.COURSE_LESSON_UPDATED_SUCCESS_MESSAGE, result)
# -----------------------------------------
