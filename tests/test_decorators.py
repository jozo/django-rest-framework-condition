import calendar
import json
from datetime import datetime

from django.urls import reverse
from django.utils.http import http_date
from rest_framework import status
from rest_framework.test import APITestCase


def to_http_date(dt):
    return http_date(calendar.timegm(dt.utctimetuple()))


CORRECT_LAST_MODIFIED_RESPONSE = to_http_date(datetime(2019, 1, 1))


class TestApiViewWithoutDecorators(APITestCase):
    def test_no_header_is_added_to_response(self):
        url = reverse('api-view-no-condition')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')
        assert not response.has_header('ETag')

    def test_last_modified_header_from_request_is_ignored(self):
        url = reverse('api-view-no-condition')
        response = self.client.get(url,
                                   HTTP_IF_NONE_MATCH='"hash123"',
                                   HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')
        assert not response.has_header('ETag')


class TestViewSetWithoutDecorators(APITestCase):
    def test_list_no_header_is_added_to_response(self):
        url = reverse('no-condition-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')
        assert not response.has_header('ETag')

    def test_list_last_modified_header_from_request_is_ignored(self):
        url = reverse('no-condition-list')
        response = self.client.get(url,
                                   HTTP_IF_NONE_MATCH='"hash123"',
                                   HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2010, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition'}
        assert not response.has_header('Last-Modified')
        assert not response.has_header('ETag')

    def test_detail_no_header_is_added_to_response(self):
        url = reverse('no-condition-detail', args=[123])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition', 'pk': '123'}
        assert not response.has_header('Last-Modified')
        assert not response.has_header('ETag')

    def test_detail_last_modified_header_from_request_is_ignored(self):
        url = reverse('no-condition-detail', args=[123])
        response = self.client.get(url,
                                   HTTP_IF_NONE_MATCH='"hash123"',
                                   HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2010, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'data': 'no-condition', 'pk': '123'}
        assert not response.has_header('Last-Modified')
        assert not response.has_header('ETag')


class TestLastModifiedWithApiView(APITestCase):
    def test_header_is_added_to_response(self):
        url = reverse('api-view-last-modified')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.data == {'data': '2019'}

    def test_returns_full_response_if_last_modified_from_request_is_before_server_last_modified(self):
        url = reverse('api-view-last-modified')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.data == {'data': '2019'}

    def test_returns_304_response_if_last_modified_from_request_is_after_server_last_modified(self):
        url = reverse('api-view-last-modified')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2222, 1, 5)))
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.status_code == status.HTTP_304_NOT_MODIFIED


class TestLastModifiedWithViewSetList(APITestCase):
    def test_header_is_added_to_response(self):
        url = reverse('last-modified-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.data == {'data': '2019'}

    def test_returns_full_response_if_last_modified_from_request_is_before_server_last_modified(self):
        url = reverse('last-modified-list')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.data == {'data': '2019'}

    def test_returns_304_response_if_last_modified_from_request_is_after_server_last_modified(self):
        url = reverse('last-modified-list')
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2222, 1, 5)))
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.status_code == status.HTTP_304_NOT_MODIFIED


class TestLastModifiedWithViewSetDetail(APITestCase):
    def test_header_is_added_to_response(self):
        url = reverse('last-modified-detail', args=[123])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.data == {'data': '2019', 'pk': '123'}

    def test_returns_full_response_if_last_modified_from_request_is_before_server_last_modified(self):
        url = reverse('last-modified-detail', args=[123])
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2009, 1, 1)))
        assert response.status_code == status.HTTP_200_OK
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.data == {'data': '2019', 'pk': '123'}

    def test_returns_304_response_if_last_modified_from_request_is_after_server_last_modified(self):
        url = reverse('last-modified-detail', args=[123])
        response = self.client.get(url, HTTP_IF_MODIFIED_SINCE=to_http_date(datetime(2222, 1, 5)))
        assert response['Last-Modified'] == CORRECT_LAST_MODIFIED_RESPONSE
        assert response.status_code == status.HTTP_304_NOT_MODIFIED


class TestEtagWithApiView(APITestCase):
    def test_etag_is_added_to_response(self):
        url = reverse('api-view-etag')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['ETag'] == '"hash123"'
        assert response.data == {'data': 'etag'}

    def test_returns_full_response_if_etag_does_not_match(self):
        url = reverse('api-view-etag')
        response = self.client.get(url, HTTP_IF_NONE_MATCH='"we-do-not-match"')
        assert response.status_code == status.HTTP_200_OK
        assert response['ETag'] == '"hash123"'
        assert response.data == {'data': 'etag'}

    def test_returns_304_if_etag_match(self):
        url = reverse('api-view-etag')
        response = self.client.get(url, HTTP_IF_NONE_MATCH='"hash123"')
        assert response.status_code == status.HTTP_304_NOT_MODIFIED
        assert response['ETag'] == '"hash123"'


class TestEtagWithViewSetList(APITestCase):
    def test_etag_is_added_to_response(self):
        url = reverse('etag-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['ETag'] == '"hash123"'
        assert response.data == {'data': 'etag'}

    def test_returns_full_response_if_etag_does_not_match(self):
        url = reverse('etag-list')
        response = self.client.get(url, HTTP_IF_NONE_MATCH='"we-do-not-match"')
        assert response.status_code == status.HTTP_200_OK
        assert response['ETag'] == '"hash123"'
        assert response.data == {'data': 'etag'}

    def test_returns_304_if_etag_match(self):
        url = reverse('etag-list')
        response = self.client.get(url, HTTP_IF_NONE_MATCH='"hash123"')
        assert response.status_code == status.HTTP_304_NOT_MODIFIED
        assert response['ETag'] == '"hash123"'


class TestEtagWithViewSetDetail(APITestCase):
    def test_etag_is_added_to_response(self):
        url = reverse('etag-detail', args=[123])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['ETag'] == '"hash123"'
        assert response.data == {'data': 'etag', 'pk': '123'}

    def test_returns_full_response_if_etag_does_not_match(self):
        url = reverse('etag-detail', args=[123])
        response = self.client.get(url, HTTP_IF_NONE_MATCH='"we-do-not-match"')
        assert response.status_code == status.HTTP_200_OK
        assert response['ETag'] == '"hash123"'
        assert response.data == {'data': 'etag', 'pk': '123'}

    def test_returns_304_if_etag_match(self):
        url = reverse('etag-detail', args=[123])
        response = self.client.get(url, HTTP_IF_NONE_MATCH='"hash123"')
        assert response.status_code == status.HTTP_304_NOT_MODIFIED
        assert response['ETag'] == '"hash123"'

    def test_etag_has_access_to_kwargs_from_view(self):
        url = reverse('etag-kwargs-detail', args=[42])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['ETag'] == '"hash-42"'
        assert response.data == {'data': 'etag', 'pk': '42'}


class TestDecoratorMatchesBuiltin(APITestCase):
    def check_responses(self, builtin_url, api_url):
        builtin_response = self.client.get(builtin_url)
        api_response = self.client.get(api_url)

        assert builtin_response.status_code == api_response.status_code
        assert json.loads(builtin_response.content) == api_response.data

        # Check the headers added, but DRF is allowed to add additional
        # headers, and the content length may differ.
        for key in builtin_response._headers:
            if key.lower() != 'content-length':
                assert builtin_response[key] == api_response[key]

    def test_etag(self):
        self.check_responses(
            builtin_url=reverse('builtin-view-etag'),
            api_url=reverse('api-view-etag'))

    def test_etag_with_kwargs(self):
        self.check_responses(
            builtin_url=reverse('builtin-view-etag-kwargs', args=[42]),
            api_url=reverse('etag-kwargs-detail', args=[42]))

    def test_last_modified(self):
        self.check_responses(
            builtin_url=reverse('builtin-view-last-modified'),
            api_url=reverse('api-view-last-modified'))
