from datetime import datetime

from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.response import Response

from django.views.decorators.http import (
    etag as builtin_etag,
    last_modified as builtin_last_modified,
)
from rest_framework_condition import etag, last_modified


def my_last_modified(self, request, *args, **kwargs):
    return datetime(2019, 1, 1)


def my_etag(self, request, *args, **kwargs):
    return 'hash123'


def etag_from_kwargs(self, request, *args, **kwargs):
    return 'hash-{}'.format(kwargs['pk'])


@builtin_last_modified(lambda request: my_last_modified(None, request))
def builtin_last_modified_view(request):
    return JsonResponse({'data': '2019'})


@builtin_etag(lambda request: my_etag(None, request))
def builtin_etag_view(request):
    return JsonResponse({'data': 'etag'})


@builtin_etag(
    lambda request, **kwargs: etag_from_kwargs(None, request, **kwargs))
def builtin_etag_kwargs_view(request, pk):
    return JsonResponse({'data': 'etag', 'pk': pk})


class NoConditionApiView(views.APIView):
    def get(self, request):
        return Response({'data': 'no-condition'})


class LastModifiedApiView(views.APIView):
    @last_modified(my_last_modified, use_self=True)
    def get(self, request):
        return Response({'data': '2019'})


class ETagApiView(views.APIView):
    @etag(my_etag, use_self=True)
    def get(self, request):
        return Response({'data': 'etag'})


class NoConditionViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({'data': 'no-condition'})

    def retrieve(self, request, pk=None):
        return Response({'data': 'no-condition', 'pk': pk})


class LastModifiedViewSet(viewsets.ViewSet):
    @last_modified(my_last_modified, use_self=True)
    def list(self, request):
        return Response({'data': '2019'})

    @last_modified(my_last_modified, use_self=True)
    def retrieve(self, request, pk=None):
        return Response({'data': '2019', 'pk': pk})


class EtagViewSet(viewsets.ViewSet):
    @etag(my_etag, use_self=True)
    def list(self, request):
        return Response({'data': 'etag'})

    @etag(my_etag, use_self=True)
    def retrieve(self, request, pk=None):
        return Response({'data': 'etag', 'pk': pk})


class EtagFromKwargsViewSet(viewsets.ViewSet):
    @etag(etag_from_kwargs, use_self=True)
    def retrieve(self, request, pk=None):
        return Response({'data': 'etag', 'pk': pk})
