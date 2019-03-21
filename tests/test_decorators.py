import calendar
from datetime import datetime

from django.urls import reverse
from django.utils.http import http_date
from rest_framework import status
from rest_framework.test import APITestCase


def test_assert_true():
    assert True

# test:
# - etag headers


def to_http_date(dt):
    return http_date(calendar.timegm(dt.utctimetuple()))


class TestApiViewWithoutDecorators(APITestCase):
    def test_no_header_is_added_to_response(self):
        url = reverse('api-view-no-condition')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')
        # TODO add for etags everywhere

    def test_last_modified_header_from_request_is_ignored(self):
        url = reverse('api-view-no-condition')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')


class TestViewSetWithoutDecorators(APITestCase):
    def test_list_no_header_is_added_to_response(self):
        url = reverse('no-condition-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')

    def test_list_last_modified_header_from_request_is_ignored(self):
        url = reverse('no-condition-list')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2010, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')

    def test_detail_no_header_is_added_to_response(self):
        url = reverse('no-condition-detail', args=[123])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition', 'pk': '123'}
        assert not response.has_header('Last-Modified')

    def test_detail_last_modified_header_from_request_is_ignored(self):
        url = reverse('no-condition-detail', args=[123])
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2010, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition', 'pk': '123'}
        assert not response.has_header('Last-Modified')


class TestLastModifiedWithApiView(APITestCase):
    def test_header_is_added_to_response(self):
        url = reverse('api-view-last-modified')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': '2019'}
        assert response.has_header('Last-Modified')

    def test_returns_full_response_if_last_modified_from_request_is_before_server_last_modified(self):
        url = reverse('api-view-last-modified')
        response = self.client.get(url, data=None, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': '2019'}
        assert response.has_header('Last-Modified')

    def test_returns_304_response_if_last_modified_from_request_is_after_server_last_modified(self):
        url = reverse('api-view-last-modified')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2222, 1, 5)))
        assert response.status_code == status.HTTP_304_NOT_MODIFIED
        assert response.has_header('Last-Modified')


class TestLastModifiedWithViewSetList(APITestCase):
    def test_decorator_no_header(self):
        url = reverse('last-modified-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': '2019'}
        assert response.has_header('Last-Modified')

    def test_decorator_with_header_before(self):
        url = reverse('last-modified-list')
        response = self.client.get(url, data=None, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': '2019'}
        assert response.has_header('Last-Modified')

    def test_decorator_with_header_after(self):
        url = reverse('last-modified-list')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2222, 1, 5)))
        assert response.status_code == status.HTTP_304_NOT_MODIFIED
        assert response.has_header('Last-Modified')


class TestLastModifiedWithViewSetDetail(APITestCase):
    def test_decorator_no_header(self):
        url = reverse('last-modified-detail', args=[123])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': '2019', 'pk': '123'}
        assert response.has_header('Last-Modified')

    def test_decorator_with_header_before(self):
        url = reverse('last-modified-detail', args=[123])
        response = self.client.get(url, data=None, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': '2019', 'pk': '123'}
        assert response.has_header('Last-Modified')

    def test_decorator_with_header_after(self):
        url = reverse('last-modified-detail', args=[123])
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2222, 1, 5)))
        assert response.status_code == status.HTTP_304_NOT_MODIFIED
        assert response.has_header('Last-Modified')
