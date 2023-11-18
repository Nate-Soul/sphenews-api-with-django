from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
   Custom permission to allow access only to the owner.
    """
    pass

class IsEditor(permissions.BasePermission):
    """
   Custom permission to allow access only to the editors.
    """
    pass

class IsAdmin(permissions.BasePermission):
    """
   Custom permission to allow access only to the admin.
    """
    pass

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to only the owner or admin
    """
    pass

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow access to owner or admin but grants access to anonymous users to read content
    """
    pass
                
    

class IsOwnerOrEditorOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to owner, editors and admins    
    """
    pass

class IsOwnerOrEditorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to anyone (GET), but allows access to owner, editors or admins
    """
    
    pass