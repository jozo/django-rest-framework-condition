from django import VERSION
from tests.views import View2010, ViewUnwrapped


if VERSION < (2, 0, 0):
    from django.conf.urls import url
    urlpatterns = [
        url('^test_app/2010/$', View2010.as_view(), name='view2010'),
        url('^test_app/unwrapped/$', ViewUnwrapped.as_view(), name='view-unwrapped'),
    ]
else:
    from django.urls import path
    urlpatterns = [
        path('^test_app/2010/$', View2010.as_view(), name='view2010'),
        path('^test_app/unwrapped/$', ViewUnwrapped.as_view(), name='view-unwrapped'),
    ]

