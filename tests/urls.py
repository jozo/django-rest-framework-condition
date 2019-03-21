from django import VERSION
from tests.views import LastModifiedApiView, NoConditionApiView, NoConditionUserViewSet, LastModifiedUserViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('no-condition', NoConditionUserViewSet, basename='no-condition')
router.register('last-modified', LastModifiedUserViewSet, basename='last-modified')

if VERSION < (2, 0, 0):
    from django.conf.urls import url, include
    urlpatterns = [
        url('^api-view/no-condition/$', NoConditionApiView.as_view(), name='api-view-no-condition'),
        url('^api-view/last-modified/$', LastModifiedApiView.as_view(), name='api-view-last-modified'),
        url('^view-set/', include(router.urls))
    ]
else:
    from django.urls import path, include
    urlpatterns = [
        path('^api-view/no-condition/$', NoConditionApiView.as_view(), name='api-view-no-condition'),
        path('^api-view/last-modified/$', LastModifiedApiView.as_view(), name='api-view-last-modified'),
        path('^view-set/', include(router.urls))
    ]

