from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from nativo_english.api.shared import messages
from nativo_english.api.shared.auth.views import is_token_present_in_header

class IsTeacherUserRole(permissions.BasePermission):
    """
    Custom permission to only allow access to users with an 'admin' role.
    """

    def has_permission(self, request, view):
        user_role = None
        token = None
        # try:
            # Extract the token from the Authorization header
        token = is_token_present_in_header(request)

        if not token:
              raise AuthenticationFailed("Authorization token is missing.")

            # Use JWTAuthentication to validate the token and retrieve the user's role
        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        user_role = validated_token.get('role')  # Extract 'role' from JWT payload
        
        if user_role == 'teacher':
            return True
        
        # Raise a permission denied exception with a custom message
        raise PermissionDenied(detail=messages.PERMISSION_DENIED_MESSAGE)