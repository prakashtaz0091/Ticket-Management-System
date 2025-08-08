from rest_framework.permissions import BasePermission
from core.utils import has_permission

class HasManageStatusPermission(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "can_manage_status")


class HasManagePriorityPermission(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "can_manage_priority")
    
    
class HasTicketPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return has_permission(request.user, 'can_create_ticket')
        if view.action in ['update', 'partial_update']:
            return has_permission(request.user, 'can_edit_ticket')
        if view.action == 'destroy':
            return has_permission(request.user, 'can_delete_ticket')
        return True


class HasMenuPermission(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "can_manage_menus")
