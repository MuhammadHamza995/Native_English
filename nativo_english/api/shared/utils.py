from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError, NotFound

from rest_framework_simplejwt.exceptions import TokenError

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
def api_exception_handler(exc, context):
    # Convert Django Http404 to DRF NotFound
    if isinstance(exc, Http404):
        exc = NotFound(detail=str(exc))

    # Handle DoesNotExist exceptions
    if isinstance(exc, ObjectDoesNotExist):
        exc = exception_handler(exc, context)

     # Handle TokenError explicitly
    if isinstance(exc, TokenError):
        # Customize the error message for TokenError
        custom_message = 'Token is blacklisted or invalid'
        return Response({
            'status': 'error',
            'status_code': status.HTTP_400_BAD_REQUEST,
            'message': custom_message
        }, status=status.HTTP_400_BAD_REQUEST)

    response = exception_handler(exc, context)
    
    if response is not None:
        # Default custom message
        custom_message = response.data.get('detail', 'An error occurred')

        # Customize response structure
        response.data = {
            'status': 'error',
            'status_code': response.status_code,
            'message': custom_message if not isinstance(custom_message, list) else custom_message[0],
        }
         
        if response is not None:
            if isinstance(exc, AuthenticationFailed):
                response.data['status_code'] = status.HTTP_401_UNAUTHORIZED
            elif isinstance(exc, PermissionDenied):
                response.data['status_code'] = status.HTTP_403_FORBIDDEN
            elif isinstance(exc, NotAuthenticated):
                response.data['status_code'] = status.HTTP_401_UNAUTHORIZED
            elif isinstance(exc, ValidationError):
                response.data['status_code'] = status.HTTP_400_BAD_REQUEST
                # response.data['message'] = custom_message[0]
            elif isinstance(exc, NotFound):
                response.data['status_code'] = status.HTTP_404_NOT_FOUND
                # response.data['message'] = custom_message[0]
            elif isinstance(exc, TokenError):
                response.data['status_code'] = status.HTTP_400_BAD_REQUEST
            else:
                response.data['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            
    return response