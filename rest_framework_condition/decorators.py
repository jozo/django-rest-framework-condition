import functools
import warnings

from calendar import timegm

from django.utils.cache import get_conditional_response
from django.utils.http import http_date, quote_etag


def condition(etag_func=None, last_modified_func=None, use_self=False):
    """
    Decorator to support conditional retrieval (or change) for a Django Rest
    Framework's ViewSet.

    This decorator emulates Django's original decorator by wrapping the
    underlying functionality where possible but handles the Django Rest
    Framework request object.

    See: django.views.decorators.http.condition
    """

    if not use_self:
        warnings.warn(
            'The etag_func and last_modified_func should accept a "self" '
            'argument which matches how Django Rest Framework calls '
            'view/viewset methods.\n\n'
            'After updating the handlers pass "use_self" to the condition '
            'decorator to enable the future functionality and silence this '
            'warning.',
            DeprecationWarning)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if etag_func:
                if use_self:
                    etag = etag_func(self, request, *args, **kwargs)
                else:
                    etag = etag_func(request, *args, **kwargs)

                # The value from etag_func() could be quoted or unquoted.
                if etag:
                    etag = quote_etag(etag)
            else:
                etag = None

            if last_modified_func:
                if use_self:
                    last_modified = last_modified_func(
                        self, request, *args, **kwargs)
                else:
                    last_modified = last_modified_func(
                        request, *args, **kwargs)

                if last_modified:
                    last_modified = timegm(last_modified.utctimetuple())
            else:
                last_modified = None

            # pass the wrapped WSGI request for Django
            response = get_conditional_response(
                request._request,
                etag=etag,
                last_modified=last_modified,
            )

            if response is None:
                response = func(self, request, *args, **kwargs)

            # Set relevant headers on the response if they don't already exist
            # and if the request method is safe.
            if request.method in ('GET', 'HEAD'):
                if last_modified and not response.has_header('Last-Modified'):
                    response['Last-Modified'] = http_date(last_modified)
                if etag:
                    response.setdefault('ETag', etag)

            return response

        return wrapper
    return decorator


# Shortcut decorators for common cases based on ETag or Last-Modified only
def etag(etag_func, use_self=False):
    return condition(etag_func=etag_func, use_self=use_self)


def last_modified(last_modified_func, use_self=False):
    return condition(last_modified_func=last_modified_func, use_self=use_self)
