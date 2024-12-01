from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError

# Creating API Response Handler
def api_response(status_code, message, data=None):
    response_data = {
        "status": "success" if status_code < 400 else "error",
        "status_code": status_code,
        "message": message,
    }
    
    # Check if user has passed some data for response
    if data is not None:
        response_data["data"] = data
    
    return Response(response_data, status=status_code)


# Creating API Exception Handler
from rest_framework import status

def api_exception_handler(exc, context):
    # Use DRF's default exception handler
    response = exception_handler(exc, context)

    # Fallback response for unhandled exceptions
    if response is None:
        return Response(
            {
                'status': 'error',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'An unexpected error occurred.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Ensure response.data exists
    if hasattr(response, 'data') and isinstance(response.data, dict):
        custom_message = response.data.get('detail', 'An error occurred')
        response.data = {
            'status': 'error',
            'status_code': response.status_code,
            'message': custom_message
        }

    # Customize response for specific exceptions
    if isinstance(exc, AuthenticationFailed):
        response.data['status_code'] = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, PermissionDenied):
        response.data['status_code'] = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, NotAuthenticated):
        response.data['status_code'] = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, ValidationError):
        response.data['status_code'] = status.HTTP_400_BAD_REQUEST
        # Handle list messages from ValidationError
        if isinstance(custom_message, list) and custom_message:
            response.data['message'] = custom_message[0]
    else:
        response.data['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR

    return response