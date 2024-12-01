# Define OpenAPI schema components for better readability
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from nativo_english.api.shared.swagger_sample_responses import SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE

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
    'tags': ['AdminCourse'],
    'summary': 'Create a New Course (Admin access only)',
    'operation_id': 'create_new_course_by_admin',
    'description': 'Creates a new course by an Admin User. Requires course title, description, and paid status.',
    # 'request': {
    #     'application/json': {
    #         'schema': {
    #             'type': 'object',
    #             'properties': {
    #                 'title': {'type': 'string', 'description': 'Title of the course (required, max 100 characters)'},
    #                 'is_paid': {'type': 'boolean', 'description': 'Whether the course is paid or free (required)'},
    #                 'description': {'type': 'string', 'description': 'Detailed description of the course'},
    #             },
    #             'required': ['title', 'is_paid'],
    #         }
    #     }
    # },
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
    'summary': 'Creates a new course section (Admin access only)',
    'operation_id': 'create_new_course_section',
    'description': 'Allows an admin user to create a new course section.',
    # 'request': {
    #     'application/json': {
    #         'example': {
    #             'title': 'New Section Title',
    #             'course_id': 101,
    #             'description': 'Description of the new course section.',
    #         }
    #     }
    # },
    'responses': {
    201: OpenApiResponse(
        description='Course Section Created Successfully',
        response={
            'application/json': {
                'status': {'type': 'integer', 'example': 200},
                'message': {'type': 'string', 'example': 'Course section created successfully.'},
                'data': {
                    'id': {'type': 'integer', 'example': 1},
                    'title': {'type': 'string', 'example': 'New Section Title'},
                    'course_id': {'type': 'integer', 'example': 101},
                    'description': {'type': 'string', 'example': 'Description of the new course section.'},
                }
            }
        }
    ),
    400: OpenApiResponse(
        description='Bad Request - Validation Errors or Issues Creating Course Section',
        response={
            'application/json': {
                'status': {'type': 'integer', 'example': 400},
                'message': {'type': 'string', 'example': 'Validation error occurred.'},
                'errors': {
                    'title': {'type': 'array', 'items': {'type': 'string'}, 'example': ['This field is required.']},
                    'course_id': {'type': 'array', 'items': {'type': 'string'}, 'example': ['Invalid ID provided.']},
                }
            }
        }
    ),
},}


GET_ADMIN_COURSE_SECTION_DETAIL_BY_ID_SCHEMA = {
    'tags': ['AdminCourseSection'],
    'summary': "Retrieve Course Section by ID (Admin access only)",
    'operation_id': 'get_course_section_detail_by_id',
    'responses': {
        200: OpenApiResponse(
            description="Course Section Retrieved Successfully",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string', 'example': 'Course Section Retrieved Successfully'},
                    'data': {
                        'id': {'type': 'integer', 'example': 1},
                        'title': {'type': 'string', 'example': 'Introduction to Python'},
                        'course_id': {'type': 'integer', 'example': 101},
                        'description': {'type': 'string', 'example': 'This is the introductory section of the Python course.'},
                    }
                }
            }
        ),
        404: OpenApiResponse(
            description="Course Section Not Found",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 404},
                    'message': {'type': 'string', 'example': 'Course section not found'},
                }
            }
        ),
    }
}


UPDATE_ADMIN_COURSE_SECTION_BY_ID_SCHEMA = {
    'tags': ['AdminCourseSection'],
    'summary': "Update Course Section by ID (Admin access only)",
    'operation_id': 'update_course_section_by_id',
    'description': 'Allows an admin user to update details of a course section by its ID.',
    # 'request': {
    #     'application/json': {
    #         'example': {
    #             'title': 'Updated Section Title',
    #             'course_id': 101,
    #             'description': 'Updated section description.',
    #         }
    #     }
    # },
    'responses': {
        200: OpenApiResponse(
            description="Course Section Updated Successfully",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 200},
                    'message': {'type': 'string', 'example': 'Course section updated successfully.'},
                    'data': {
                        'id': {'type': 'integer', 'example': 1},
                        'title': {'type': 'string', 'example': 'Updated Section Title'},
                        'course_id': {'type': 'integer', 'example': 101},
                        'description': {'type': 'string', 'example': 'Updated section description.'},
                    }
                }
            }
        ),
        400: OpenApiResponse(
            description="Bad Request - Validation Errors",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 400},
                    'message': {'type': 'string', 'example': 'Validation Error'},
                    'errors': {
                        'title': {'type': 'array', 'items': {'type': 'string'}, 'example': ['This field is required.']},
                        'course_id': {'type': 'array', 'items': {'type': 'string'}, 'example': ['Invalid ID provided.']},
                    }
                }
            }
        ),
        404: OpenApiResponse(
            description="Course Section Not Found",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 404},
                    'message': {'type': 'string', 'example': 'Course section with the given ID does not exist.'}
                }
            }
        )
    }
}

# --------------------------------------------



# --------------------------------------------
# Get All courses Lessons by Admin Schema
# --------------------------------------------
GET_ADMIN_ALL_COURSE_LESSON_RETRIEVE_SCHEMA = {
    'tags': ['AdminCourseLesson'],
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
    'tags': ['AdminCourseLesson'],
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
    'tags': ['AdminCourseLesson'],
    'summary': 'Creates a new course lesson (Can be accessed by user with admin role only)',
    'operation_id': 'create_course_lesson',
    'description': 'Creates a new course lesson by Admin User.',
    'responses': {
        201: OpenApiResponse(
            description="Course Lesson Created Successfully",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 201},
                    'message': {'type': 'string', 'example': "Course Lesson Created Successfully"},
                    'data': {
                        'id': {'type': 'integer', 'example': 1},
                        'title': {'type': 'string', 'example': 'Lesson Title'},
                        'course_section_id': {'type': 'integer', 'example': 42},
                        'content': {'type': 'string', 'example': 'Lesson Content Description'},
                    }
                }
            }
        ),
        400: OpenApiResponse(
            description="Bad Request - Validation Errors",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 400},
                    'message': {'type': 'string', 'example': "Validation Error"},
                    'errors': {
                        'title': {'type': 'array', 'items': {'type': 'string'}, 'example': ['This field is required.']},
                        'course_section_id': {'type': 'array', 'items': {'type': 'string'}, 'example': ['Invalid ID provided.']},
                    }
                }
            }
        ),
        401: OpenApiResponse(
            description="Unauthorized Access - Admin Role Required",
            response={
                'application/json': {
                    'status': {'type': 'integer', 'example': 401},
                    'message': {'type': 'string', 'example': "You are not authorized to perform this action."}
                }
            }
        ),
    }
}

UPDATE_ADMIN_COURSE_LESSON_UPDATE_SCHEMA = {
    'tags': ['AdminCourseLesson'],
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