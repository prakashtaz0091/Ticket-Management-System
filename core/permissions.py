from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)


def has_permission(user, resource_to_access, action_to_perform):
    if not user.is_authenticated:
        return False
    try:
        role = user.profile.role
    except Exception as e:
        logger.warning(f"User profile or role error: {e}")
        return False
    else:
        permissions = role.permissions.prefetch_related("actions").all()
        for permission in permissions:
            if f"{resource_to_access}:{action_to_perform}" in permission.actions_list:
                return True
        return False


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        resource = view.basename
        action = view.action
        return has_permission(
            request.user, resource_to_access=resource, action_to_perform=action
        )
