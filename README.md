# django-rest-framework-condition

[![Build Status](https://travis-ci.com/jozo/django-rest-framework-condition.svg?branch=master)](https://travis-ci.com/jozo/django-rest-framework-condition)
[![codecov](https://codecov.io/gh/jozo/django-rest-framework-condition/branch/master/graph/badge.svg)](https://codecov.io/gh/jozo/django-rest-framework-condition)


This package allows you to use [`@condition`](https://docs.djangoproject.com/en/2.1/topics/conditional-view-processing/) decorator from Django on ViewSet or
APIView from Django Rest Framework. In other words, you can use http headers 
ETag and Last-modified with you APIs.

It doesn't create custom implementation of etags or last-modified header but uses ones from Django which means you can be sure it will be updated by Django's authors. 

Similarly as in Django you can use shortcut decorators `@last_modified` and
`@etag`.

Tested with:
* Python: 3.7, 3.8, 3.9
* Django: 2.2, 3.1, 3.2
* Django Rest Framework: 3.11, 3.12


Installation
------------

```bash
pip install django-rest-framework-condition
```


Usage
-----

Use decorators same way as with Django views.

**Last-modified example**

```python
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_condition import last_modified


class LastModifiedApiView(APIView):
    @last_modified(lambda _: datetime(2019, 1, 1))
    def get(self, request):
        return Response({'data': 'I have Last-Modified header!'})
```

**ETag example**

```python
import hashlib

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_condition import etag


def my_etag(request, *args, **kwargs):
    return hashlib.md5(':'.join(request.GET.dict().values()).encode('utf-8')).hexdigest()


class EtagApiView(APIView):
    @etag(my_etag)
    def get(self, request):
        return Response({'data': 'I have Etag!'})
```

**Both ETag and Last-Modified example**

```python
import hashlib
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_condition import condition


def my_etag(request, *args, **kwargs):
    return hashlib.md5(':'.join(request.GET.dict().values()).encode('utf-8')).hexdigest()


def my_last_modified(request, *args, **kwargs):
    return datetime(2019, 1, 1)


class ConditionApiView(APIView):
    @condition(etag_func=my_etag, last_modified_func=my_last_modified)
    def get(self, request):
        return Response({'data': 'I have both Last-Modified and Etag!'})
```
