import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_comment_list_unauthenticated():
    """
    Test that unauthenticated users can access the comments list.
    """
    client = APIClient()
    url = reverse('comment')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_comment_post_unauthenticated():
    """
    Test that unauthenticated users cannot post a comment.
    """
    client = APIClient()
    url = reverse('comment')
    data = {'content': 'This is a test comment.'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data
    assert response.data['detail'] == 'Authentication credentials were not provided.'
