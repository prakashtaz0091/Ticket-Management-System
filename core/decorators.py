from django.shortcuts import render
from .utils import has_permission

def permission_required(permission_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not has_permission(request.user, permission_name):
                return render(request, "core/not-authorized.html", status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
