from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


def owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if request.user.role != 'owner':
            return HttpResponseForbidden('شما اجازه دسترسی به این بخش را ندارید.')
        return view_func(request, *args, **kwargs)
    return wrapper