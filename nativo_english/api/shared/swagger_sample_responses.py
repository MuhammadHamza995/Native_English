from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE = {
    '400': OpenApiResponse(
        description='Bad request due to invalid parameters',
        response={
            'type': 'object',
            'properties': {
                'status': {'type': 'string'},
                'status_code': {'type': 'integer'},
                'message': {'type': 'string'}
            }
        },
        examples=[
            OpenApiExample(
                'Bad Request',
                value={
                    'status_code': 400,
                    'status': 'error',
                    'message': 'Bad request due to invalid parameters'
                }
            )
        ]
    ),

    '401': OpenApiResponse(
        description='Invalid Access token or Unauthenticated user',
        response={
            'type': 'object',
            'properties': {
                'status_code': {'type': 'integer'},
                'status': {'type': 'string'},
                'message': {'type': 'string'}
            }
        },
        examples=[
            OpenApiExample(
                'Invalid Access token',
                value={
                    'status_code': 401,
                    'status': 'error',
                    'message': 'Given token not valid for any token type'
                }
            ),
            OpenApiExample(
                'Unauthenticated user',
                value={
                    'status_code': 401,
                    'status': 'error',
                    'message': 'Authentication credentials were not provided.'
                }
            )
        ]
    ),

    '404': OpenApiResponse(
        description='User not found',
        response={
            'type': 'object',
            'properties': {
                'status_code': {'type': 'integer', 'example': 404},  # Added status_code
                'status': {'type': 'string', 'example': 'error'},
                'message': {'type': 'string', 'example': 'User not found.'},
            },
        },
        examples=[
            OpenApiExample(
                'User not found',
                value={
                    'status_code': 404,
                    'status': 'error',
                    'message': 'User not found.'
                }
            )
        ]
    ),
}

