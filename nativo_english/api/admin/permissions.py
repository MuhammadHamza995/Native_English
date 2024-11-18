from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from nativo_english.api.shared import messages

class IsAdminUserRole(permissions.BasePermission):
    """
    Custom permission to only allow access to users with an 'admin' role.
    """

    def has_permission(self, request, view):
        user_role = None
        token = None
        try:
            # Extract the token from the Authorization header
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            
            if not token:
                raise AuthenticationFailed("Authorization token is missing.")

            token = auth_header.split(' ')[1]

            # Use JWTAuthentication to validate the token and retrieve the user's role
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user_role = validated_token.get('role')  # Extract 'role' from JWT payload
        
        except AuthenticationFailed as auth_error:
            # Handle cases where token is missing, invalid, or expired
            raise AuthenticationFailed("Invalid or expired token. Please log in again.")
        except Exception as e:
            # Catch other unexpected errors
            print(f"Token validation error: {e}")
            raise AuthenticationFailed("An error occurred during token validation.")
        
        if user_role == 'admin':
            return True
        
        # Raise a permission denied exception with a custom message
        raise PermissionDenied(detail=messages.PERMISSION_DENIED_MESSAGE)
    
