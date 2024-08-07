# favourites/tests.py
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_favourite_list_unauthenticated():
    """
    Test that unauthenticated users cannot access the favourites list.
    """
    client = APIClient()
    url = reverse('favourite-list-create')
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data
    assert response.data['detail'] == 'Authentication credentials were not provided.'
