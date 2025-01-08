# Define OpenAPI schema components for better readability
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.openapi import OpenApiRequest
from nativo_english.api.shared.swagger_sample_responses import SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE, SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE_FOR_COURSE
from nativo_english.api.shared import messages
from nativo_english.api.shared.auth.views import ResendOtpRequestSerializer
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


#---------------------------------------------------
# RESEND_OTP_SCHEMA
#---------------------------------------------------
RESEND_OTP_SCHEMA = {
    'tags': ['User Authentication'],
    'operation_id': 'resend_otp',
    'summary': 'Resend OTP to user',
    'description': (
        'This endpoint allows resending an OTP to a user if 2FA is enabled. '
        'It validates the user ID and ensures that previous OTPs are marked as used.'
    ),
    'responses': {
        200: OpenApiResponse(
            description='OTP resent successfully.',
            response={
                'type': 'object',
                'properties': {
                    'status_code': {'type': 'integer', 'example': 200},
                    'status': {'type': 'string', 'example': 'success'},
                    'message': {'type': 'string', 'example': 'OTP has been resent successfully.'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'user_id': {'type': 'integer', 'example': 1},
                            'role': {'type': 'string', 'example': 'admin'},
                        },
                    },
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
        401: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['401'],
    },
}

#-------------------------------------------------------
# FORGOT_PASSWORD_SCHEMA
#-------------------------------------------------------
FORGOT_PASSWORD_SCHEMA = {
    'tags': ['User Authentication'],
    'operation_id': 'forgot_password',
    'summary': 'Send password reset link',
    'description': 'Send a password reset link to the provided email if the user exists.',
    'request': OpenApiRequest(
        {
            'type': 'object',
            'properties': {
                'email': {
                    'type': 'string',
                    'example': 'example@example.com',
                    'description': 'The email address of the user.',
                },
            },
            'required': ['email'],
        }
    ),
    'responses': {
        200: OpenApiResponse(
            description='Successful response',
            response={
                'type': 'object',
                'properties': {
                    'status_code': {'type': 'integer', 'example': 200},
                    'status': {'type': 'string', 'example': 'success'},
                    'message': {'type': 'string', 'example': 'Password reset link sent to your email'},
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
        404: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['404'],
    },
}

#------------------------------------------------------------
# RESET_PASSWORD_SCHEMA
#------------------------------------------------------------
UPDATE_PASSWORD_SCHEMA = {
    "tags": ["User Authentication"],
    "operation_id": "update_password",
    "summary": "Update the user's password using token and user ID.",
    "description": "This endpoint allows a user to update their password by providing a valid UID, token, and new password.",
    "request": {
        "application/json": {
            "type": "object",
            "properties": {
                "uid": {
                    "type": "string",
                    "description": "Base64 encoded user ID",
                    "example": "MjQ",
                },
                "token": {
                    "type": "string",
                    "description": "Password reset token",
                    "example": "f8g-as89-1k2",
                },
                "password": {
                    "type": "string",
                    "description": "New password to set",
                    "example": "NewSecurePassword123",
                },
            },
            "required": ["uid", "token", "password"],
        }
    },
    "responses": {
        200: OpenApiResponse(
            description="Password updated successfully.",
            response={
                "type": "object",
                "properties": {
                    "status_code": {"type": "integer", "example": 200},
                    "message": {"type": "string", "example": "Password updated successfully."},
                },
            },
        ),
        400: SWAGGER_ERROR_SAMPLE_RESPONSES_ADMIN_ROLE['400'],
    },
}




