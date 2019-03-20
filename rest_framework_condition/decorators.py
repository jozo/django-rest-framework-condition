import functools
from django.views.decorators.http import condition as django_condition


def condition(etag_func=None, last_modified_func=None):
    """
    Decorator to support conditional retrieval (or change)
    for a Django Rest Framework's ViewSet.

    It calls Django's original decorator but pass correct request object to it.
    Django's original decorator doesn't work with DRF request object.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(obj_self, request, *args, **kwargs):
            drf_request = request
            wsgi_request = request._request

            def patched_viewset_method(*_args, **_kwargs):
                """Call original viewset method with correct type of request"""
                return func(obj_self, drf_request, *args, **kwargs)

            django_decorator = django_condition(etag_func, last_modified_func)
            decorated_viewset_method = django_decorator(patched_viewset_method)
            return decorated_viewset_method(wsgi_request)
        return wrapper
    return decorator


# Shortcut decorators for common cases based on ETag or Last-Modified only
def etag(etag_func):
    return condition(etag_func=etag_func)


def last_modified(last_modified_func):
    return condition(last_modified_func=last_modified_func)
