import calendar
from datetime import datetime

from django.urls import reverse
from django.utils.http import http_date
from rest_framework import status
from rest_framework.test import APITestCase


def test_assert_true():
    assert True

# test:
# - no decorator
# - decorator last-modified headers
# - etag headers


def to_http_date(dt):
    return http_date(calendar.timegm(dt.utctimetuple()))


class LastModifiedTests(APITestCase):
    def test_no_decorator_no_header(self):
        url = reverse('view-unwrapped')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'key': 'unwrapped'})

    def test_no_decorator_with_header(self):
        url = reverse('view-unwrapped')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2010, 1, 1)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'key': 'unwrapped'})

    def test_decorator_no_header(self):
        url = reverse('view2010')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'key': '2010'})

    def test_decorator_with_header_before(self):
        url = reverse('view2010')
        response = self.client.get(url, data=None, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'key': '2010'})

    def test_decorator_with_header_after(self):
        url = reverse('view2010')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2014, 1, 5)))
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)
