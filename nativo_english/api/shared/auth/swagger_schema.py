# Define OpenAPI schema components for better readability
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from nativo_english.api.shared.swagger_sample_responses import SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE, SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE_FOR_COURSE
from nativo_english.api.shared import messages

# --------------------------------------------
# 2FA - PATCH Schema
# --------------------------------------------
FA2_UPDATE_SCHEMA = {
    'tags': ['2FA-Config'],
    'operation_id': 'update_user_2FA_config',
    'summary': 'Enable or disable 2FA for User',
    'description': 'Enable or disable 2FA for User',

    'responses': {
        200: OpenApiResponse(
            description='Successful response with updated user data',
            response={
                'type': 'object',
                'properties': {
                    'status_code': {'type': 'integer', 'example': 200},
                    'status': {'type': 'string', 'example': 'success'},
                    'message': {'type': 'string', 'example': '2FA settings updated successfully.'},

                    'data': {
                        'type': 'object',
                        'properties': {
                            'enable_2fa': {
                                'type': 'string',
                                'example': True
                            }
                        },
                    },
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
        401: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['401'],
    },
}

# --------------------------------------------
# 2FA - VERIFY_OTP_SCHEMA
# --------------------------------------------
VERIFY_OTP_SCHEMA = {
    'tags': ['OTP-2FA-VERIFY'],
    'operation_id': 'verify_2FA_otp',
    'summary': 'Verify (OTP) 2FA for User',
    'description': 'Verify (OTP) 2FA for User',

    'responses': {
        200: OpenApiResponse(
            description='Successful response with access tokens',
            response={
                'type': 'object',
                'properties': {
                    'status_code': {'type': 'integer', 'example': 200},
                    'status': {'type': 'string', 'example': 'success'},
                    'message': {'type': 'string', 'example': 'Login Successful'},

                    'data': {
                        'type': 'object',
                        'properties': {
                            'refresh': {
                                'type': 'string',
                                'example': 'e9ad8f9ahjchiashdiasyiwqyeiowahdksjdkcsuidfuasoidusaiojdklasjdlksa'
                            },
                            'access': {
                                'type': 'string',
                                'example': 'e9ad8f9ahjchiashdiasyiwqyeiowahdksjdkcsuidfuasoidusaiojdklasjdlksa'
                            },
                            'enable_2fa': {
                                'type': 'string',
                                'example': True
                            }
                        },
                    },
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
        401: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['401'],
    },
}