from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAdminUserRole(permissions.BasePermission):
    """
    Custom permission to only allow access to users with an 'admin' role.
    """
    
    def has_permission(self, request, view):
        # Retrieve role from JWT payload
        user_role = request.user.token.get('role') if hasattr(request.user, 'token') else None

        if user_role == 'admin':
            return True
        else:
            # Raise a permission denied exception with custom message
            raise PermissionDenied(detail="You do not have permission to perform this action.")