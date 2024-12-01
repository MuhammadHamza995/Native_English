from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied, ValidationError
from django.db import connection

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
    response = exception_handler(exc, context)

    custom_message = response.data.get('detail', 'An error occurred')
    
    response.data = {
        'status': 'error',
        'status_code' : status.HTTP_401_UNAUTHORIZED,
        'message': custom_message
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
            response.data['message'] = custom_message[0]
        else:
            response.data['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            
    return response


def get_course_lesson_content_by_id(course_lesson_id):
    """
    Fetches course lesson content by its ID using a PL/SQL procedure.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("""
                BEGIN 
                    :result := get_course_lesson_content_by_id(:id);
                END;
            """, {
                'id': course_lesson_id,
                'result': cursor.var(type_code=..., size=...),  
            })
            result = cursor.fetchone()
            if not result:
                return None  # Handle case where no data is returned
            return {
                'id': result[0],
                'title': result[1],
                'content': result[2],
                'created_at': result[3],
            }
        except Exception as e:
            raise ValueError(f"Error fetching data: {e}")
