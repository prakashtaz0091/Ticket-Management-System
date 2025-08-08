def has_permission(user, permission_name):
    if not user.is_authenticated:
        return False
    if hasattr(user, "userprofile") and user.userprofile.role:
        return user.userprofile.role.permissions.filter(name=permission_name).exists()
    return False
