# shared/course/views.py
from django.shortcuts import get_object_or_404
from .models import Course,CourseSection, CourseLesson
from .serializer import CourseSerializer, CourseSectionSerializer, CourseLessonSerializer
from .models import Course,CourseSection, CourseLesson
from rest_framework.exceptions import NotFound
from nativo_english.api.shared.db_helper import call_plpgsql_function
from django.core.exceptions import ValidationError
from nativo_english.api.shared.upload_engine import handle_file_upload
from nativo_english.api.shared.course.models import LessonContent
from nativo_english.api.shared.course.serializer import  LessonContentSerializer
#--------- COURSE --------------

def create_course(request):

    """
    Creates a new Course instance from the provided data.

    This function validates the provided data using CourseSerializer. If valid, it creates a new
    Course and returns the serialized course data. If validation fails, returns the errors.

    Args:
        data (dict): A dictionary containing course information for creation.

    Returns:
        dict: Serialized course data if creation is successful; otherwise, validation errors.
    """

    try:
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save(created_by=request.user, modified_by=request.user)
            return CourseSerializer(course).data
        return serializer.errors 
    
    except Exception as ex:
        raise ex

def get_all_courses(filter_title=None, filter_is_paid=None):

    """
    Retrieves a list of Course instances, optionally filtered by name or payment status.

    This function fetches all Course instances from the database and applies optional filters:
    - If `filter_title` is provided, filters the courses by title (case-insensitive, partial match).
    - If `filter_is_paid` is provided, filters the courses based on whether they are paid.

    Args:
        filter_title (str, optional): A string to filter courses by title. Defaults to None.
        filter_is_paid (bool, optional): A boolean to filter courses by payment status (e.g., free or paid).
                                         Defaults to None.

    Returns:
        list: A list of serialized course data. Each item in the list represents a course and its details.
    """

    # queryset = Course.objects.all()
    queryset = Course.objects.filter(is_active=True)
    if filter_title:
        queryset = queryset.filter(title__icontains=filter_title)
    
    if filter_is_paid is not None:
        filter_is_paid = str(filter_is_paid).lower() == 'true'
        queryset = queryset.filter(is_paid=filter_is_paid)
        
    return CourseSerializer(queryset, many=True).data

def get_course_by_id(course_id):

    """
    Retrieves a Course instance by its ID.

    Fetches a single Course instance matching the provided course ID.
    Raises a 404 error if the course does not exist.

    Args:
        course_id (int): The unique identifier of the course.

    Returns:
        dict: Serialized course data if the course exists.

    Raises:
        Http404: If the course with the given ID does not exist.
    """

    try:
        if course_id is not None:
            course = get_object_or_404(Course, id=course_id, is_active=True)
            return CourseSerializer(course).data
    except Exception as ex:
        raise ex

def update_course(course_id, request):

    """
    Updates an existing Course instance with the provided data.

    Fetches the course instance by ID, then updates it with the given data using CourseSerializer.
    Returns the updated course data if successful, or validation errors if the update fails.

    Args:
        course_id (int): The unique identifier of the course to update.
        data (dict): A dictionary containing the updated course information.

    Returns:
        dict: Serialized course data if the update is successful; otherwise, validation errors.

    Raises:
        Http404: If the course with the given ID does not exist.
    """

    try:
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(modified_by=request.user)
            return serializer.data
        return serializer.errors 
    
    except Exception as ex:
        raise ex


def get_all_courses_with_pagination(page_num, page_size, title, mode, is_paid, is_active, search_query, sort_field, sort_order, owner_id):
    """
    Retrieves a list of Course instances, optionally filtered by name or payment status.

    This function fetches all Course instances from the database and applies optional filters:
    - If `filter_title` is provided, filters the courses by title (case-insensitive, partial match).
    - If `filter_is_paid` is provided, filters the courses based on whether they are paid.
    - if `search_query` is provided, filters the courses by title / description with that search query
    - if `sort_field` is provided, sort the data based on that field
    - if `sort_direction` is provided, sort the data base on the filed and provided direction

    Args:
        filter_title (str, optional): A string to filter courses by title. Defaults to None.
        filter_is_paid (bool, optional): A boolean to filter courses by payment status (e.g., free or paid).
                                         Defaults to None.

    Returns:
        list: A list of serialized course data. Each item in the list represents a course and its details.
    """
    try:
        all_courses_results = call_plpgsql_function('courses_list_with_pagination_get', 
            page_num, page_size, title, mode, is_paid, is_active, search_query, sort_field, sort_order, owner_id
        )

        # Prepare the response
        courses_data = [
            {
                'course_id': row['course_id'],
                'title': row['title'],
                'description': row['description'],
                'is_paid': row['is_paid'],
                'price': row['price'],
                'mode': row['mode'],
                'avg_rating': row['avg_rating'],
                'is_active': row['is_active'],
                'owner_name': row['owner_name'],
                'owner': row['owner'],
                'enrollment_count': row['enrollment_count'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'modified_by': row['updated_by_name'],

            }
            for row in all_courses_results
        ]     
        
        total_count = all_courses_results[-1]['total_count'] if all_courses_results else 0  # Extract the total count from the last column
        total_pages = (total_count + page_size - 1) // page_size  # Calculate total pages
        response_data = {
            'courses': courses_data,
            'total_count': total_count,
            'total_pages': total_pages,
            'current_page': page_num,
            'page_size': page_size
        }
        
        # return all_courses_results
        return response_data
    
    except Exception as ex:
        raise ex


def get_course_detail_by_id(course_id, owner_id=None):
    """
    Retrieves a Course instance by its ID.

    Fetches a single Course instance matching the provided course ID.
    Raises a 404 error if the course does not exist.

    Args:
        course_id (int): The unique identifier of the course.

    Returns:
        dict: Serialized course data if the course exists.

    """
    
    try:
        course_details = call_plpgsql_function('course_detail_by_id_get', course_id, owner_id)
        response_data = {
                'course_id': course_details[0]['course_id'],
                'title': course_details[0]['title'],
                'description': course_details[0]['description'],
                'is_paid': course_details[0]['is_paid'],
                'price': course_details[0]['price'],
                'mode': course_details[0]['mode'],
                'avg_rating': course_details[0]['avg_rating'],
                'is_active': course_details[0]['is_active'],
                'owner_name': course_details[0]['owner_name'],
                'enrollment_count': course_details[0]['enrollment_count'],
                'created_at': course_details[0]['created_at'],
                'created_by': course_details[0]['created_by_name'],
                'updated_at': course_details[0]['updated_at'],
                'modified_by': course_details[0]['updated_by_name'],

        }

        return response_data
        
    except Exception as ex:
        raise ex


#--------- COURSE SECTION  --------------

def create_course_section(data):

    """
    Creates a new Course Section instance from the provided data.

    This function validates the provided data using CourseSectionSerializer. If valid, it creates a new
    Course Section and returns the serialized course data. If validation fails, returns the errors.

    Args:
        data (dict): A dictionary containing course section information for creation.

    Returns:
        dict: Serialized course section data if creation is successful; otherwise, validation errors.
    """

    try:
        serializer = CourseSectionSerializer(data=data)
        if serializer.is_valid():
            course_section = serializer.save()
            return CourseSectionSerializer(course_section).data
        # return serializer.errors 
        return {"errors": serializer.errors}
    
    except Exception as ex:
        raise ex

def get_all_course_sections(filter_title=None, course_id=None):
    """
    Fetch course sections by PL/pgSQL function or Django ORM based on the input filters.
    """
    if course_id:
        # Call the PL/pgSQL function to fetch sections by course_id
        sections = call_plpgsql_function('course_section_by_course_id_get', course_id)

        if not sections:
            raise NotFound("No course sections found for the given course ID.")
    else:
        queryset = CourseSection.objects.all()

        if filter_title:
            queryset = queryset.filter(section_title__icontains=filter_title)

        sections = CourseSectionSerializer(queryset, many=True).data

    return sections

def get_course_section_by_id(course_section_id):

    """
    Retrieves a Course Section instance by its ID.

    Fetches a single Course Section instance matching the provided course section ID.
    Raises a 404 error if the course section does not exist.

    Args:
        course_section_id (int): The unique identifier of the course section.

    Returns:
        dict: Serialized course section data if the course exists.

    Raises:
        Http404: If the course section with the given ID does not exist.
    """

    try:
        if course_section_id is not None:
            course_section = get_object_or_404(CourseSection, id=course_section_id)
            return CourseSectionSerializer(course_section).data
    except Exception as ex:
        raise ex

def update_course_section(course_section_id, data):

    """
    Updates an existing Course Section instance with the provided data.

    Fetches the course section instance by ID, then updates it with the given data using CourseSectionSerializer.
    Returns the updated course section data if successful, or validation errors if the update fails.

    Args:
        course_section_id (int): The unique identifier of the course section to update.
        data (dict): A dictionary containing the updated course section information.

    Returns:
        dict: Serialized course section data if the update is successful; otherwise, validation errors.

    Raises:
        Http404: If the course section with the given ID does not exist.
    """

    try:
        course_section = get_object_or_404(CourseSection, id=course_section_id)
        serializer = CourseSectionSerializer(course_section, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors 
    
    except Exception as ex:
        raise ex


#--------- COURSE LESSON --------------

def create_course_lesson(data):

    """
    Creates a new Course Lesson instance from the provided data.

    This function validates the provided data using CourseLessonSerializer. If valid, it creates a new
    Course Lesson and returns the serialized course data. If validation fails, returns the errors.

    Args:
        data (dict): A dictionary containing course lesson information for creation.

    Returns:
        dict: Serialized course lesson data if creation is successful; otherwise, validation errors.
    """

    try:
        serializer = CourseLessonSerializer(data=data)
        if serializer.is_valid():
            course_lesson = serializer.save()
            return CourseLessonSerializer(course_lesson).data
        return serializer.errors 
    
    except Exception as ex:
        raise ex

def get_all_course_lessons(filter_title=None, course_id=None, section_id=None):
    """
    Fetch course lessons by PL/pgSQL function or Django ORM based on the input filters.
    """
    if course_id or section_id:
        # Call the PL/pgSQL function to fetch lessons by course_id or section_id
        lessons = call_plpgsql_function('course_lesson_by_course_or_section_id_get', course_id, section_id)
        lessons = [lesson for lesson in lessons if lesson['is_active']]
        if not lessons:
            raise NotFound("No active course lessons found for the given course ID or section ID.")
    else:
        queryset = CourseLesson.objects.filter(is_active=True)

        if filter_title:
            queryset = queryset.filter(lesson_title__icontains=filter_title)

        lessons = CourseLessonSerializer(queryset, many=True).data

    return lessons

def get_course_lesson_by_id(course_lesson_id):

    """
    Retrieves a Course Lesson instance by its ID.

    Fetches a single Course Lesson instance matching the provided course lesson ID.
    Raises a 404 error if the course lesson does not exist.

    Args:
        course_lesson_id (int): The unique identifier of the course lesson.

    Returns:
        dict: Serialized course lesson data if the course exists.

    Raises:
        Http404: If the course lesson with the given ID does not exist.
    """

    try:
        if course_lesson_id is not None:
            course_lesson = get_object_or_404(CourseLesson, id=course_lesson_id, is_active=True)
            return CourseLessonSerializer(course_lesson).data
    except Exception as ex:
        raise ex

def update_course_lesson(course_lesson_id, data):

    """
    Updates an existing Course Lesson instance with the provided data.

    Fetches the course lesson instance by ID, then updates it with the given data using CourseLessonSerializer.
    Returns the updated course section data if successful, or validation errors if the update fails.

    Args:
        course_lesson_id (int): The unique identifier of the course lesson to update.
        data (dict): A dictionary containing the updated course section information.

    Returns:
        dict: Serialized course lesson data if the update is successful; otherwise, validation errors.

    Raises:
        Http404: If the course lesson with the given ID does not exist.
    """

    try:
        course_lesson = get_object_or_404(CourseLesson, id=course_lesson_id)
        serializer = CourseLessonSerializer(course_lesson, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors 
    
    except Exception as ex:
        raise ex


def create_lesson_content(lesson_id, data=None, FILES=None):
    """
    Creates a new lesson content record with uploaded files.
    """
    # Fetch the CourseLesson instance using the lesson_id
    try:
        lesson = CourseLesson.objects.get(id=lesson_id)
    except CourseLesson.DoesNotExist:
        raise NotFound(f"CourseLesson with ID {lesson_id} not found.")
    
    # Handle file uploads using `upload_engine.py`
    content_video_url = None
    if 'video_url' in FILES:
        content_video_url = handle_file_upload(FILES['video_url'], allowed_extensions=['.mp4'])

    content_audio_url = None
    if 'audio' in FILES:
        content_audio_url = handle_file_upload(FILES['audio'], allowed_extensions=['.mp3'])

    content_image_url = None
    if 'image' in FILES:
        content_image_url = handle_file_upload(FILES['image'], allowed_extensions=['.jpg', '.png', '.jpeg'])

    # Extract other fields
    text = data.get('text', '')

    # Create the lesson content in the database, using the fetched CourseLesson instance
    lesson_content = LessonContent.objects.create(
        fk_course_lesson=lesson,  # Use the CourseLesson instance here
        content_video_url=content_video_url,
        content_text=text,
        content_audio_url=content_audio_url,
        content_image_url=content_image_url,
    )

    # Serialize and return the created instance
    return LessonContentSerializer(lesson_content).data


