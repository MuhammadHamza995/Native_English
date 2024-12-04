# Define OpenAPI schema components for better readability
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from nativo_english.api.shared.swagger_sample_responses import SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE, SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE_FOR_COURSE
from nativo_english.api.shared import messages



# --------------------------------------------
# Teacher Course Schema Swagger
# --------------------------------------------
GET_TEACHER_COURSE_LIST_SCHEMA = {
    'tags': ['TeacherCourse'],
    'summary': 'Get All Courses (Teacher access only)',
    'operation_id': 'get_course_list_of_teacher',
    'description': 'Lists all courses with optional filters by title and is_paid, supports pagination.',
    'parameters': [
        OpenApiParameter(
            name="page_num",
            location=OpenApiParameter.QUERY,
            description="Pagination - Page Number for data if there are so many courses in the system",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="page_size",
            location=OpenApiParameter.QUERY,
            description="Pagination - Page size, number of records to return per page",
            required=False,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="title",
            location=OpenApiParameter.QUERY,
            description="Title of the course to search from",
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name="is_paid",
            location=OpenApiParameter.QUERY,
            description="Filter by paid status, true or false (optional)",
            required=False,
            type=OpenApiTypes.BOOL,
        ),
        OpenApiParameter(
            name="is_active",
            location=OpenApiParameter.QUERY,
            description="Filter by active status, true or false (optional)",
            required=False,
            type=OpenApiTypes.BOOL,
        ),
        OpenApiParameter(
            name="mode",
            location=OpenApiParameter.QUERY,
            description="Mode - Self-paced, online",
            required=False,
            type=OpenApiTypes.STR,  # You should use STR since it's a textual value
            enum=["","self", "live"],  # These are the fixed values you want in the dropdown
            default="",  # Optional, specify the default value
        ),
        OpenApiParameter(
            name="level",
            location=OpenApiParameter.QUERY,
            description="Level - Difficulty level",
            required=False,
            type=OpenApiTypes.STR,  # You should use STR since it's a textual value
            enum=["beginner", "intermediate", "advance"],  # These are the fixed values you want in the dropdown
            default="",  # Optional, specify the default value
        ),
        OpenApiParameter(
            name="search",
            location=OpenApiParameter.QUERY,
            description="Search - Search for courses this will be helpful to integrate with search bar",
            required=False,
            type=OpenApiTypes.STR,  # You should use STR since it's a textual value
        ),
        OpenApiParameter(
            name="sort_by",
            location=OpenApiParameter.QUERY,
            description="Sort By - Sort by fields",
            required=False,
            type=OpenApiTypes.STR,  # You should use STR since it's a textual value
            enum=['course_id', 'title', 'mode', 'avg_rating', 'price', 'enrollment_count', 'created_at', 'updated_at']
        ),
        OpenApiParameter(
            name="sort_order",
            location=OpenApiParameter.QUERY,
            description="Sort order - Sort order by fields",
            required=False,
            type=OpenApiTypes.STR,  # You should use STR since it's a textual value
            enum=['DESC', 'ASC']
        )
    ],
    'responses': {
        200: OpenApiResponse(
            description='Successful response with paginated course data',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example':'success'},
                    'status_code': {'type': 'integer', 'example':'200'},
                    'message': {'type':'string', 'example': messages.COURSE_LIST_RETRIEVED_SUCCESS_MESSAGE},
                    'data': {'type': 'object', 'example': {
                        'courses': [{
                                "course_id": 1,
                                "title": "Math",
                                "description": "Math 101",
                                "is_paid": 'true',
                                "price": 200,
                                "mode": "self",
                                "level": "beginner",
                                "avg_rating": 0,
                                "is_active": 'true',
                                "owner_name": "John Cena",
                                "owner": 2,
                                "enrollment_count": 0,
                                "created_at": "2024-12-01T21:56:24.916322Z",
                                "updated_at": "2024-12-03T20:11:30.532890Z",
                                "modified_by": "Nativo English Admin"
                                }
                            ],
                        "total_count": 1,
                        "total_pages": 1,
                        "current_page": 1,
                        "page_size": 10  
                        }
                    }
                }
            }
        ),
        404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE_FOR_COURSE['404'],
    },
}

POST_TEACHER_COURSE_CREATE_SCHEMA = {
    'tags': ['TeacherCourse'],
    'summary': 'Create a New Course (Teacher access only)',
    'operation_id': 'create_new_course_by_teacher',
    'description': 'Creates a new course by an Teacher User. Requires course title, description, and paid status.',
    'responses': {
        201: OpenApiResponse(
            description='Course successfully created',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 201},
                    'message': {'type': 'string', 'example': 'Course created successfully.'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 101},
                            'title': {'type': 'string', 'example': 'Advanced Python Programming'},
                            'is_paid': {'type': 'boolean', 'example': True},
                            'description': {'type': 'string', 'example': 'A comprehensive course on advanced Python concepts.'},
                        },
                    },
                },
            },
        ),
        400: OpenApiResponse(
            description='Bad Request',
            response={'type': 'object', 'properties': {'message': {'type': 'string', 'example': 'Invalid data'}}},
        ),
    },
}

GET_TEACHER_COURSE_RETRIEVE_SCHEMA = {
    'tags': ['TeacherCourse'],
    'summary': 'Retrieve Course by ID (Teacher access only)',
    'operation_id': 'get_course_details_by_id_of_teacher',
    'description': 'Retrieves a course by its ID for teacher users.',
    'parameters': [
        OpenApiParameter(
            name="id",
            location=OpenApiParameter.PATH,
            description="Course ID",
            required=True,
            type=OpenApiTypes.INT
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='Course successfully retrieved',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 200},  # Added status for consistency
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'title': {'type': 'string', 'example': 'Advanced Python Programming'},
                            'is_paid': {'type': 'boolean', 'example': True},
                            'description': {'type': 'string', 'example': 'A comprehensive course on advanced Python concepts.'},
                        },
                    },
                },
            },
        ),
        404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE ['404'],
    },
}

UPDATE_TEACHER_COURSE_UPDATE_SCHEMA = {
    'tags': ['TeacherCourse'],
    'summary': 'Update course by ID (Teacher access only)',
    'operation_id': 'update_course_by_id_of_teacher',
    'description': 'Updates a course based on the provided ID and input data.',
    'parameters': [
        OpenApiParameter(
            name="id",
            location="path",  # Correct location for path parameters
            description="Course ID",
            required=True,
            type=OpenApiTypes.INT,  # Specify the type as INT
        ),
    ],
    
    'responses': {
        200: OpenApiResponse(
            description='Course successfully updated',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 200},
                    'id': {'type': 'integer'},
                    'title': {'type': 'string'},
                    'is_paid': {'type': 'boolean'},
                    'description': {'type': 'string'},
                },
            },
        ),
        400: OpenApiResponse(
            description='Bad Request',
            response={'type': 'object', 'properties': {'message': {'type': 'string', 'example': 'Invalid data'}}},
        ),
    },
}
# --------------------------------------------


# --------------------------------------------
# Get All courses Section by Admin Schema
# --------------------------------------------
# GET_ADMIN_COURSE_ALL_SECTION_SCHEMA = {
#     'tags': ['AdminCourseSection'],
#     'summary': 'Get All Courses Sections (Admin access only)',
#     'operation_id': 'get_course_section_list',
#     'description': 'Lists all courses sections with optional filters by title and course_id.',
#     'parameters': [
#         OpenApiParameter(
#             name="title",
#             location=OpenApiParameter.QUERY,
#             description="Title of the course section to filter by (optional).",
#             required=False,
#             type=OpenApiTypes.STR
#         ),
#         OpenApiParameter(
#             name="page",
#             location=OpenApiParameter.QUERY,
#             description="Page number for paginated results (optional).",
#             required=False,
#             type=OpenApiTypes.INT
#         ),
#     ]
# }

# POST_ADMIN_COURSE_SECTION_CREATE_SCHEMA = {
#     'tags': ['AdminCourseSection'],
#     'summary': 'Creates a new course section (Can be accessed by user with admin role only)',
#     'operation_id': 'create_new_course_section',
#     'description': 'Creates a new course section by Admin User.',
# }

# GET_ADMIN_COURSE_SECTION_DETAIL_BY_ID_SCHEMA = {
#     'tags': ['AdminCourseSection'],
#     'summary': "Retrieve Course Section by ID (Admin access only)",
#     'operation_id': 'get_course_section_detail_by_id'
# }

# UPDATE_ADMIN_COURSE_SECTION_BY_ID_SCHEMA = {
#     'tags': ['AdminCourseSection'],
#     'summary': "Update Course Section by ID (Admin access only)",
#     'operation_id': 'update_course_section_detail_by_id'
# }
# # --------------------------------------------



# # --------------------------------------------
# # Get All courses Lessons by Admin Schema
# # --------------------------------------------
# GET_ADMIN_ALL_COURSE_LESSON_RETRIEVE_SCHEMA = {
#     'tags': ['AdminCourseSectionLesson'],
#     'summary': 'Get All Courses Lessons (Admin access only)',
#     'description': 'Lists all courses lessons with optional filters by title, section_id and course_id.',
#     'operation_id': 'get_course_lesson_list',
#     'parameters': [
#         OpenApiParameter(
#             name="title",
#             location=OpenApiParameter.QUERY,
#             description="Title of the course section to filter by (optional).",
#             required=False,
#             type=OpenApiTypes.STR
#         ),
#         OpenApiParameter(
#             name="page",
#             location=OpenApiParameter.QUERY,
#             description="Page number for paginated results (optional).",
#             required=False,
#             type=OpenApiTypes.INT
#         ),
#     ]
# }

# GET_ADMIN_COURSE_LESSON_RETRIEVE_SCHEMA = {
#     'tags': ['AdminCourseSectionLesson'],
#     'summary': 'Retrieve Course Lesson by ID (Admin access only)',
#     'operation_id': 'get_course_lesson_details_by_id',
#     'description': 'Retrieves a course lesson by its ID for admin users.',
#     'responses': {
#         200: OpenApiResponse(
#             description='Course successfully retrieved',
#             response={
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'integer', 'example': 200},  # Added status for consistency
#                     'data': {
#                         'type': 'object',
#                         'properties': {
#                             'id': {'type': 'integer', 'example': 1},
#                             'title': {'type': 'string', 'example': 'Advanced Python Programming'},
#                             'is_paid': {'type': 'boolean', 'example': True},
#                             'description': {'type': 'string', 'example': 'A comprehensive course on advanced Python concepts.'},
#                         },
#                     },
#                 },
#             },
#         ),
#         404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE ['404'],
#     },
# }

# POST_ADMIN_COURSE_LESSON_CREATE_SCHEMA = {
#     'tags': ['AdminCourseSectionLesson'],
#     'summary': 'Creates a new course lesson (Can be accessed by user with admin role only)',
#     'operation_id': 'create_course_lesson',
#     'description': 'Creates a new course lesson by Admin User.',
# }

# UPDATE_ADMIN_COURSE_LESSON_UPDATE_SCHEMA = {
#     'tags': ['AdminCourseSectionLesson'],
#     'summary': 'Update course lesson by ID (Admin access only)',
#     'operation_id': 'update_course_lesson_by_id',
#     'description': 'Updates a course lesson based on the provided ID and input data.',
    
#     'responses': {
#         200: OpenApiResponse(
#             description='Course successfully updated',
#             response={
#                 'type': 'object',
#                 'properties': {
#                     'status': {'type': 'integer', 'example': 200},
#                     'id': {'type': 'integer'},
#                     'title': {'type': 'string'},
#                     'is_paid': {'type': 'boolean'},
#                     'description': {'type': 'string'},
#                 },
#             },
#         ),
#         400: OpenApiResponse(
#             description='Bad Request',
#             response={'type': 'object', 'properties': {'message': {'type': 'string', 'example': 'Invalid data'}}},
#         ),
#     },
# }
# # --------------------------------------------


# # --------------------------------------------
# # Get All courses lesson content by Admin Schema
# # --------------------------------------------
# GET_ADMIN_COURSE_ALL_LESSON_CONTENT_SCHEMA = {
#     'tags': ['AdminCourseSectionLessonContent'],
#     'summary': 'Get All Lesson content (Admin access only)',
#     'operation_id': 'get_lesson_content_list',
#     'description': 'Lists all lesson content'
# }