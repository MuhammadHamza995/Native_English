# Define OpenAPI schema components for better readability
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from nativo_english.api.shared.swagger_sample_responses import SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE, SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE_FOR_COURSE
from nativo_english.api.shared import messages

# --------------------------------------------
# Users Swagger Schema Admin
# --------------------------------------------
GET_USER_LIST_SCHEMA = {
    'tags': ['Admin'],
    'operation_id': 'get_users_list',
    'summary': 'Get All users (Can be accessed by user with admin role only)',
    'description': 'Lists all users (if filter is applied for role/suspend)',
    'parameters': [
        OpenApiParameter(
            name='role',
            location=OpenApiParameter.QUERY,
            description='Role of the user to filter by (optional)',
            required=False,
            type=OpenApiTypes.STR,
        ),
        OpenApiParameter(
            name='is_active',
            location=OpenApiParameter.QUERY,
            description='Filter by active status, true or false (optional)',
            required=False,
            type=OpenApiTypes.BOOL,
        ),
        OpenApiParameter(
            name='page',
            location=OpenApiParameter.QUERY,
            description='Get other pages data, pass the page number',
            required=False,
            type=OpenApiTypes.INT,
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='Successful response with paginated user data',
            response={
                'type': 'object',
                'properties': {
                    'count': {'type': 'integer'},
                    'num_pages': {'type': 'integer'},
                    'current_page': {'type': 'integer'},
                    'results': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'username': {'type': 'string'},
                                'email': {'type': 'string'},
                                'first_name': {'type': 'string'},
                                'last_name': {'type': 'string'},
                                'is_active': {'type': 'boolean'},
                            },
                        },
                    },
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
        401: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['401'],
    },
}

POST_USER_SCHEMA = {
    'tags': ['Admin'],
    'operation_id': 'creates_new_user_by_admin',
    'summary': 'Creates a new User (Can be accessed by user with admin role only)',
    'description': 'Creates a new user by Admin User.',
    
    'responses': {
        201: OpenApiResponse(
            description='User created successfully.',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 201},
                    'message': {'type': 'string', 'example': 'User created successfully.'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'description': 'Unique ID of the user.'},
                            'username': {'type': 'string', 'description': 'Username of the user.'},
                            'email': {'type': 'string', 'description': 'Email of the user.'},
                        },
                    },
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
    },
}


GET_USER_BY_ID_SCHEMA = {
    'tags': ['Admin'],
    'operation_id': 'get_user_detail_by_id',
    'summary': 'Retrieve User by ID (Admin role required)',
    'description': 'Retrieves a specific user by their ID. Can be accessed only by users with the admin role.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            description='User ID to retrieve',
            required=True,
            type=OpenApiTypes.INT,
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='Successful response with user details',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string', 'example': 'User retrieved successfully.'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'},
                            'email': {'type': 'string'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'is_active': {'type': 'boolean'},
                        },
                    },
                },
            },
        ),
        404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE ['404'],
        401: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE ['401'],
    },
}

UPDATE_USER_BY_ID_SCHEMA = {
    'tags': ['Admin'],
    'summary': 'Update User by ID (Admin role required)',
    'operation_id': 'update_user_info_by_id',
    'description': 'Updates the details of a specific user by their ID. Can be accessed only by users with the admin role.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location='path',  # Define the parameter as a path parameter
            description='User ID to update',
            required=True,
            type=OpenApiTypes.INT,
        ),
    ],
    
    'responses': {
        200: OpenApiResponse(
            description='User updated successfully',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string', 'example': 'User updated successfully.'},
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
        404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['404'],
        401: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['401'],
    },
}

UPDATE_USER_ROLE_SCHEMA = {
    'tags': ['Admin'],
    'summary': 'Update User Role (Admin role required)',
    'operation_id': 'update_specific_user_role',
    'description': 'Updates the role of a specific user by their ID. Can only be accessed by users with the admin role.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location='path',  # Correctly specify the parameter location
            description='User ID whose role needs to be updated',
            required=True,
            type=OpenApiTypes.INT,
        ),
    ],
    
    'responses': {
        200: OpenApiResponse(
            description='Successful response when the user role is updated',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string', 'example': 'User role updated successfully for ID: 123.'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 123},
                            'username': {'type': 'string', 'example': 'johndoe'},
                            'email': {'type': 'string', 'example': 'johndoe@example.com'},
                            'role': {'type': 'string', 'example': 'Admin'},
                        },
                    },
                },
            },
        ),
        400: OpenApiResponse(description='Bad request - Invalid input'),
        404: OpenApiResponse(description='User not found'),
        401: OpenApiResponse(description='Unauthorized request'),
    },
}

UPDATE_USER_STATUS_SCHEMA = {
    'tags': ['Admin'],
    'summary': 'update_user_status_by_admin',
    'description': 'Updates the `is_active` status of a user by their ID to either activate or suspend them.',
    'parameters': [
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            description='User ID whose status needs to be updated',
            required=True,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name='action',
            location=OpenApiParameter.PATH,
            description="Action to perform: 'activate' or 'suspend'",
            required=True,
            type=OpenApiTypes.STR,
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='User status updated successfully',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 200},
                    'message': {
                        'type': 'string',
                        'example': 'User successfully activated/suspended for ID: 123.',
                    },
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 123},
                            'username': {'type': 'string', 'example': 'john_doe'},
                            'email': {'type': 'string', 'example': 'john_doe@example.com'},
                            'is_active': {'type': 'boolean', 'example': True},
                        },
                    },
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
        404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['404'],
        401: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['401'],
    },
}
# --------------------------------------------


# --------------------------------------------
# Admin Course Schema Swagger
# --------------------------------------------
GET_ADMIN_COURSE_LIST_SCHEMA = {
    'tags': ['AdminCourse'],
    'summary': 'Get All Courses (Admin access only)',
    'operation_id': 'get_course_list',
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
        ),
        OpenApiParameter(
            name="filter_owner_id",
            location=OpenApiParameter.QUERY,
            description="Course Owner - Will return the courses of specific owner / teacher",
            required=False,
            type=OpenApiTypes.INT,
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
                                "avg_rating": 0,
                                "is_active": 'true',
                                "owner_name": "John Cena",
                                "owner": 2,
                                "enrollment_count": 0
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

POST_ADMIN_COURSE_CREATE_SCHEMA = {
    'tags': ['AdminCourse'],
    'summary': 'Create a New Course (Admin access only)',
    'operation_id': 'create_new_course_by_admin',
    'description': 'Creates a new course by an Admin User. Requires course title, description, and paid status.',
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

GET_ADMIN_COURSE_RETRIEVE_SCHEMA = {
    'tags': ['AdminCourse'],
    'summary': 'Retrieve Course by ID (Admin access only)',
    'operation_id': 'get_course_details_by_id',
    'description': 'Retrieves a course by its ID for admin users.',
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

UPDATE_ADMIN_COURSE_UPDATE_SCHEMA = {
    'tags': ['AdminCourse'],
    'summary': 'Update course by ID (Admin access only)',
    'operation_id': 'update_course_by_id',
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
GET_ADMIN_COURSE_ALL_SECTION_SCHEMA = {
    'tags': ['AdminCourseSection'],
    'summary': 'Get All Courses Sections (Admin access only)',
    'operation_id': 'get_course_section_list',
    'description': 'Lists all courses sections with optional filters by title and course_id.',
    'parameters': [
        OpenApiParameter(
            name="title",
            location=OpenApiParameter.QUERY,
            description="Title of the course section to filter by (optional).",
            required=False,
            type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name="course_id",
            location=OpenApiParameter.QUERY,
            description="ID of the course to retrieve associated sections (optional).",
            required=False,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name="page",
            location=OpenApiParameter.QUERY,
            description="Page number for paginated results (optional).",
            required=False,
            type=OpenApiTypes.INT
        ),
    ]
}

POST_ADMIN_COURSE_SECTION_CREATE_SCHEMA = {
    'tags': ['AdminCourseSection'],
    'summary': 'Creates a new course section (Can be accessed by user with admin role only)',
    'operation_id': 'create_new_course_section',
    'description': 'Creates a new course section by Admin User.',
}

GET_ADMIN_COURSE_SECTION_DETAIL_BY_ID_SCHEMA = {
    'tags': ['AdminCourseSection'],
    'summary': "Retrieve Course Section by ID (Admin access only)",
    'operation_id': 'get_course_section_detail_by_id'
}

UPDATE_ADMIN_COURSE_SECTION_BY_ID_SCHEMA = {
    'tags': ['AdminCourseSection'],
    'summary': "Update Course Section by ID (Admin access only)",
    'operation_id': 'update_course_section_detail_by_id'
}
# --------------------------------------------



# --------------------------------------------
# Get All courses Lessons by Admin Schema
# --------------------------------------------
GET_ADMIN_ALL_COURSE_LESSON_RETRIEVE_SCHEMA = {
    'tags': ['AdminCourseSectionLesson'],
    'summary': 'Get All Courses Lessons (Admin access only)',
    'description': 'Lists all courses lessons with optional filters by title, section_id and course_id.',
    'operation_id': 'get_course_lesson_list',
    'parameters': [
        OpenApiParameter(
            name="title",
            location=OpenApiParameter.QUERY,
            description="Title of the course section to filter by (optional).",
            required=False,
            type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name="course_id",
            location=OpenApiParameter.QUERY,
            description="ID of the course to retrieve associated lessons (optional).",
            required=False,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name="section_id",
            location=OpenApiParameter.QUERY,
            description="ID of the section to retrieve associated lessons (optional).",
            required=False,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name="page",
            location=OpenApiParameter.QUERY,
            description="Page number for paginated results (optional).",
            required=False,
            type=OpenApiTypes.INT
        ),
    ]
}

GET_ADMIN_COURSE_LESSON_RETRIEVE_SCHEMA = {
    'tags': ['AdminCourseSectionLesson'],
    'summary': 'Retrieve Course Lesson by ID (Admin access only)',
    'operation_id': 'get_course_lesson_details_by_id',
    'description': 'Retrieves a course lesson by its ID for admin users.',
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

POST_ADMIN_COURSE_LESSON_CREATE_SCHEMA = {
    'tags': ['AdminCourseSectionLesson'],
    'summary': 'Creates a new course lesson (Can be accessed by user with admin role only)',
    'operation_id': 'create_course_lesson',
    'description': 'Creates a new course lesson by Admin User.',
}

UPDATE_ADMIN_COURSE_LESSON_UPDATE_SCHEMA = {
    'tags': ['AdminCourseSectionLesson'],
    'summary': 'Update course lesson by ID (Admin access only)',
    'operation_id': 'update_course_lesson_by_id',
    'description': 'Updates a course lesson based on the provided ID and input data.',
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
# Get All courses lesson content by Admin Schema
# --------------------------------------------
GET_ADMIN_COURSE_ALL_LESSON_CONTENT_SCHEMA = {
    'tags': ['AdminCourseSectionLessonContent'],
    'summary': 'Get All Lesson content (Admin access only)',
    'operation_id': 'get_lesson_content_list',
    'description': 'Lists all lesson content'
}

#-----------------------------------------------


#-----------------------------------------------
# Upload the course lesson content by Admin Schema 
#-----------------------------------------------

# schema.py

POST_ADMIN_COURSE_LESSON_CONTENT_CREATE_SCHEMA = {
    'tags': ['AdminCourseSectionLessonContent'],
    'summary': 'Create a new lesson content (Admin access only)',
    'operation_id': 'create_lesson_content',
    'description': 'Create a new lesson content for a course lesson, with optional text, audio, image, and video URL.',
    'parameters': [
        OpenApiParameter(
            name="lesson_id",
            location="path",  # lesson_id is now a path parameter
            description="ID of the lesson the content belongs to",
            required=True,
            type=OpenApiTypes.INT,  # Ensure the type is set as integer
        ),
    ],
    'request': {
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                    'description': 'Text content for the lesson'
                },
                'audio': {
                    'type': 'string',
                    'format': 'uri',
                    'description': 'URL or path of the audio file'
                },
                'image': {
                    'type': 'string',
                    'format': 'uri',
                    'description': 'URL or path of the image'
                },
                'video_url': {
                    'type': 'string',
                    'format': 'uri',
                    'description': 'URL or path of the video file'
                },
            },
        },
    },
    'responses': {
        201: OpenApiResponse(
            description='Lesson content created successfully',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 201},
                    'id': {'type': 'integer'},
                    'lesson_id': {'type': 'integer'},
                    'text': {'type': 'string'},
                    'audio': {'type': 'string'},
                    'image': {'type': 'string'},
                    'video_url': {'type': 'string'},
                },
            },
        ),
        400: OpenApiResponse(
            description='Bad Request',
            response={
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Invalid data'},
                },
            },
        ),
    },
}

