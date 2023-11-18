from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from accounts.utils import verify_access_token


class IsLoggedIn(permissions.BasePermission):
    """
    Custom permissions to allow acess to logged in users
    """
    def has_permission(self, request, view):
        try:
            verify_access_token(request)
            return request.user and request.user.role in ['author', 'editor', 'admin']
        except AuthenticationFailed:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.role in ['author', 'editor', 'admin']


class IsLoggedInOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to anyone (GET), but require users to be logged in for other actions.
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        try:
            verify_access_token(request)
            return request.user and request.user.role in ['author', 'editor', 'admin']
        except AuthenticationFailed:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.role in ['author', 'editor', 'admin']

class IsOwner(permissions.BasePermission):
    """
   Custom permission to allow access only to the owner.
    """
   
    def has_object_permission(self, request, view, obj):
        try:
            verify_access_token(request)
            return obj.user == request.user
        except AuthenticationFailed:
            return False

class IsEditor(permissions.BasePermission):
    """
   Custom permission to allow access only to the editors.
    """
    
    def has_object_permission(self, request, view, obj):
        try:
            verify_access_token(request)
            return request.user and request.user.role == 'editor'
        except AuthenticationFailed:
            return False

class IsAdmin(permissions.BasePermission):
    """
   Custom permission to allow access only to the admin.
    """
    
    def has_permission(self, request, view):
        try:
            verify_access_token(request)
            return request.user and request.user.role == 'admin'
        except AuthenticationFailed:
            return False
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.role == 'admin'

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to only the owner or admin
    """
    
    def has_object_permission(self, request, view, obj):
        try:
            verify_access_token(request)
        except AuthenticationFailed:
            return False
        
        return (request.user and request.user.role == 'admin') or obj.user == request.user

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow access to owner or admin but grants access to anonymous users to read content
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        try:
            verify_access_token(request)
            return True
        except AuthenticationFailed:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.role == 'admin'
                
    

class IsOwnerOrEditorOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to owner, editors and admins    
    """
    
    def has_object_permission(self, request, view, obj):
        try:
            verify_access_token(request)
        except AuthenticationFailed:
            return False
        
        return obj.user == request.user or request.user.role in ['editor', 'admin']

class IsOwnerOrEditorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to anyone (GET), but allows access to owner, editors or admins
    """
    
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        try:
            verify_access_token(request)
            return True
        except AuthenticationFailed:
            return False 
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.role in ['editor', 'admin']