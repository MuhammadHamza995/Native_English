# shared/course/views.py
from django.shortcuts import get_object_or_404
from .models import Course
from .serializer import CourseSerializer

def create_course(data):

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
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            course = serializer.save()
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

    queryset = Course.objects.all()
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
            course = get_object_or_404(Course, id=course_id)
            return CourseSerializer(course).data
    except Exception as ex:
        raise ex

def update_course(course_id, data):

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
        serializer = CourseSerializer(course, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors 
    
    except Exception as ex:
        raise ex
