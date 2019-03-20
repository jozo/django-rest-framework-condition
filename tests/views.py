from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_condition import condition


class View2010(APIView):
    @condition(last_modified_func=lambda _: datetime(2010, 1, 1))
    def get(self, request):
        return Response({'key': '2010'})


class ViewUnwrapped(APIView):
    def get(self, request):
        return Response({'key': 'unwrapped'})
