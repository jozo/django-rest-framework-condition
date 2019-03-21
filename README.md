# django-rest-framework-condition

[![Build Status](https://travis-ci.com/jozo/django-rest-framework-condition.svg?branch=master)](https://travis-ci.com/jozo/django-rest-framework-condition)

This package allows you to use [`@condition`](https://docs.djangoproject.com/en/2.1/topics/conditional-view-processing/) decorator from Django on ViewSet or
APIView from Django Rest Framework. In other words, you can use http headers 
ETag and Last-modified with you APIs.

Similarly as in Django you can use shortcuts decorators `@last_modified` and
`@etag`.

Tested with:
* Python: 2.7, 3.7
* Django: 1.11, 2.0, 2.1, 2.2
* Django Rest Framework: 3.9


Installation
------------
- [ ] check after publishing package on pypi

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
