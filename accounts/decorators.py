
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

def require_pending_email(session_key='pending_user_email', redirect_url='register'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.session.get(session_key):
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def require_password_change(session_key='allow_password_change', redirect_url='forgot_password'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.session.get(session_key):
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def logout_required(function=None, redirect_url='home_page'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



def logout_required(function=None, redirect_url='home_page'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def logout_required_class(redirect_url='home_page'):
    def decorator(view_class):
        return method_decorator(logout_required(redirect_url=redirect_url), name='dispatch')(view_class)
    return decorator