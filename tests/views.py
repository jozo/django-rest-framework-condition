from datetime import datetime

from rest_framework import views, viewsets
from rest_framework.response import Response

from rest_framework_condition import condition


def my_last_modified(request):
    return datetime(2019, 1, 1)


def my_etag(request):
    return 'hash123'


class NoConditionApiView(views.APIView):
    def get(self, request):
        return Response({'data': 'no-condition'})


class LastModifiedApiView(views.APIView):
    @condition(last_modified_func=my_last_modified)
    def get(self, request):
        return Response({'data': '2019'})


class ETagApiView(views.APIView):
    @condition(etag_func=my_etag)
    def get(self, request):
        return Response({'data': 'etag'})


class NoConditionViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'data': 'no-condition'})

    def retrieve(self, request, pk=None):
        return Response({'data': 'no-condition', 'pk': pk})


class LastModifiedViewSet(viewsets.ViewSet):
    @condition(last_modified_func=my_last_modified)
    def list(self, request):
        return Response({'data': '2019'})

    @condition(last_modified_func=my_last_modified)
    def retrieve(self, request, pk=None):
        return Response({'data': '2019', 'pk': pk})


class EtagViewSet(viewsets.ViewSet):
    @condition(etag_func=my_etag)
    def list(self, request):
        return Response({'data': 'etag'})

    @condition(etag_func=my_etag)
    def retrieve(self, request, pk=None):
        return Response({'data': 'etag', 'pk': pk})
