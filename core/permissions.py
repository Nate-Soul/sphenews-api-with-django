from rest_framework import permissions

class IsOWnerAndStaffOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user and request.user.is_authenticated:
            return True if request.user.is_staff or request.user.is_superuser else False
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            if obj.author == request.user and request.user.is_staff or request.user.is_superuser:
                return True
        return False
    
class IsStaffOrSuperAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view): 
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            return True if request.user.is_staff or request.user.is_superuser else False
        return False
    
# class ArticleVisibilityPermission(permissions.BasePermission):
    
#     def has_object_permission(self, request, view, obj):
        
#         if request.user.is_authenticated:
#             if obj.visibility == 'private':
#                 return request.user.is_staff or request.user.is_superuser or obj.author == request.user
#         return True


# class ArticleStatusPermission(permissions.BasePermission):
    
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_authenticated:
#             if obj.status == 'draft':
#                 return obj.author == request.user and request.user.is_staff or request.user.is_superuser
#         return True

class CanViewDraftArticle(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user or request.user.is_superuser
        return False

class CanViewPrivateArticle(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.visibility == 'private' or request.user.is_superuser
        return False
