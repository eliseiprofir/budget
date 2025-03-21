from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Permission that allows access to object owners or superusers. Superusers can access any object."""
    
    def has_permission(self, request, view):
        # Allow access only to authenticated users
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Superusers can access any object
        if request.user.is_superuser:
            return True
        
        # For regular users, check if they are the owners
        return obj.user == request.user
