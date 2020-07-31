from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tests.views import (
    builtin_etag_kwargs_view,
    builtin_etag_view,
    builtin_last_modified_view,
    ETagApiView,
    EtagFromKwargsViewSet,
    EtagViewSet,
    LastModifiedApiView,
    LastModifiedViewSet,
    NoConditionApiView,
    NoConditionViewSet,
)

router = DefaultRouter()

router.register("no-condition", NoConditionViewSet, basename="no-condition")
router.register("last-modified", LastModifiedViewSet, basename="last-modified")
router.register("etag", EtagViewSet, basename="etag")
router.register("etag-kwargs", EtagFromKwargsViewSet, basename="etag-kwargs")

urlpatterns = [
    path(
        "api-view/no-condition/",
        NoConditionApiView.as_view(),
        name="api-view-no-condition",
    ),
    path(
        "api-view/last-modified/",
        LastModifiedApiView.as_view(),
        name="api-view-last-modified",
    ),
    path("api-view/etag/", ETagApiView.as_view(), name="api-view-etag"),
    path(
        "builtin/last-modified/",
        builtin_last_modified_view,
        name="builtin-view-last-modified"
    ),
    path("builtin/etag/", builtin_etag_view, name="builtin-view-etag"),
    path(
        "builtin/etag/<pk>/",
        builtin_etag_kwargs_view,
        name="builtin-view-etag-kwargs",
    ),
    path("view-set/", include(router.urls)),
]
