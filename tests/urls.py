from django import VERSION
from rest_framework.routers import DefaultRouter

from tests.views import (
    LastModifiedApiView, NoConditionApiView, ETagApiView,
    LastModifiedViewSet, NoConditionViewSet, EtagViewSet,
)

router = DefaultRouter()
router.register('no-condition', NoConditionViewSet, basename='no-condition')
router.register('last-modified', LastModifiedViewSet, basename='last-modified')
router.register('etag', EtagViewSet, basename='etag')

if VERSION < (2, 0, 0):
    from django.conf.urls import url, include
    urlpatterns = [
        url('^api-view/no-condition/$', NoConditionApiView.as_view(), name='api-view-no-condition'),
        url('^api-view/last-modified/$', LastModifiedApiView.as_view(), name='api-view-last-modified'),
        url('^api-view/etag/$', ETagApiView.as_view(), name='api-view-etag'),
        url('^view-set/', include(router.urls))
    ]
else:
    from django.urls import path, include
    urlpatterns = [
        path('^api-view/no-condition/$', NoConditionApiView.as_view(), name='api-view-no-condition'),
        path('^api-view/last-modified/$', LastModifiedApiView.as_view(), name='api-view-last-modified'),
        path('^api-view/etag/$', ETagApiView.as_view(), name='api-view-etag'),
        path('^view-set/', include(router.urls))
    ]
