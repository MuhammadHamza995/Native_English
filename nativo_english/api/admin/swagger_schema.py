# Define OpenAPI schema components for better readability
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from nativo_english.api.shared.swagger_sample_responses import SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE




GET_USER_LIST_SCHEMA = {
    'tags': ['Admin'],
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
    'summary': 'Update User Status (Admin role required)',
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


GET_ADMIN_COURSE_LIST_SCHEMA = {
    'tags': ['Admin Course'],
    'summary': 'Get All Courses (Admin access only)',
    'description': 'Lists all courses with optional filters by title and is_paid, supports pagination.',
    'parameters': [
        OpenApiParameter(
            name="title",
            location=OpenApiParameter.QUERY,
            description="Name of the course to filter by (optional)",
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
            name="page",
            location=OpenApiParameter.QUERY,
            description="Page number to retrieve data from (optional, default: 1)",
            required=False,
            type=OpenApiTypes.INT,
            default=1  # Optional, to specify a default value for pagination
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='Successful response with paginated course data',
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
                                'title': {'type': 'string'},
                                'is_paid': {'type': 'boolean'},
                                'description': {'type': 'string'},
                            },
                        },
                    },
                },
            },
        ),
        404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE ['404'],
    },
}

POST_ADMIN_COURSE_CREATE_SCHEMA = {
    'tags': ['Admin Course'],
    'summary': 'Create a New Course (Admin access only)',
    'description': 'Creates a new course by an Admin User. Requires course title, description, and paid status.',
    'request': {
        'application/json': {
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string', 'description': 'Title of the course (required, max 100 characters)'},
                    'is_paid': {'type': 'boolean', 'description': 'Whether the course is paid or free (required)'},
                    'description': {'type': 'string', 'description': 'Detailed description of the course'},
                },
                'required': ['title', 'is_paid'],
            }
        }
    },
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
    'tags': ['Admin Course'],
    'summary': 'Retrieve Course by ID (Admin access only)',
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
    'tags': ['Admin Course'],
    'summary': 'Update course by ID (Admin access only)',
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


GET_COURSE_LESSON_CONTENT_SCHEMA = {
    'tags': ["Admin"],
    'summary': 'Retrieve Course Lesson Content by ID',
    'description': 'Fetches the details of a course lesson content by its ID.',
    'parameters': [
        OpenApiParameter(
            name="course_lesson_id",
            location=OpenApiParameter.PATH,
            description="The ID of the course lesson content",
            required=True,
            type=OpenApiTypes.INT,
        ),
    ],
    'responses': {
        200: OpenApiResponse(
            description='Course Lesson Content successfully retrieved',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 200},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'title': {'type': 'string', 'example': 'Introduction to Python'},
                            'content': {'type': 'string', 'example': 'Detailed lesson content here.'},
                            'created_at': {'type': 'string', 'format': 'date-time', 'example': '2024-01-01T10:00:00Z'},
                        },
                    },
                },
            },
        ),
        404: OpenApiResponse(
            description='Course Lesson Content not found',
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'integer', 'example': 404},
                    'message': {'type': 'string', 'example': 'Course Lesson Content not found'},
                },
            },
        ),
    },
}

UPDATE_COURSE_LESSON_CONTENT_SCHEMA = {
    "tags": ["Admin"],
    "summary": "Update Course Lesson Content by ID",
    "description": "Updates the course lesson content with new details by ID.",
    "request": {
        "application/json": {
            "example": {
                "title": "Updated Title",
                "content": "Updated content goes here",
            }
        }
    },
    "responses": {
        200: {
            "description": "Course Lesson Content updated successfully",
            "examples": {
                "application/json": {
                    "status": 200,
                    "message": "Course Lesson Content updated successfully",
                }
            },
        },
        404: {
            "description": "Course Lesson Content not found",
            "examples": {
                "application/json": {
                    "status": 404,
                    "message": "Course Lesson Content not found",
                }
            },
        },
        400: {
            "description": "Validation errors occurred",
            "examples": {
                "application/json": {
                    "status": 400,
                    "errors": {
                        "title": ["This field is required."],
                    },
                }
            },
        },
    },
}
