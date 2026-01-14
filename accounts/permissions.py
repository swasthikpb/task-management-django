from rest_framework.permissions import BasePermission


class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'SUPERADMIN']
    

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'SUPERADMIN'