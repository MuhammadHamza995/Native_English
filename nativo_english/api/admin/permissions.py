from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication

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

            # Use JWTAuthentication to get the user's role from the token
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user_role = validated_token.get('role')  # get 'role' with 'role' key in JWT
        
        except Exception as e:
            print(f"Token validation error: {e}")

        if user_role == 'admin':
            return True
        
        # Raise a permission denied exception with a custom message
        raise PermissionDenied(detail="You do not have permission to perform this action.")