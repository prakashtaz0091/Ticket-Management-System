from django.shortcuts import render

# from .utils import has_permission
from functools import wraps


# def permission_required(permission_name):
#     def decorator(view_func):
#         def _wrapped_view(request, *args, **kwargs):
#             if not has_permission(request.user, permission_name):
#                 return render(request, "core/not-authorized.html", status=403)
#             return view_func(request, *args, **kwargs)

#         return _wrapped_view

#     return decorator


# to use for @api_view, this will provide basename i.e. resource and then action, which will further be used to set action and permission
def action(resource, action_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        wrapped_view.basename = resource
        wrapped_view.action = action_name

        return wrapped_view

    return decorator
