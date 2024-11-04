from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler

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

    if response is not None:
        # Modify the response data to fit your format
        response.data = {
            "status": "error",
            "message": response.data.get('detail', 'An error occurred')[0], # type: ignore
            "data": None,
        }

    return response