import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from resources.models import Resource

@pytest.mark.django_db
def test_resource_list_unauthenticated():
    """
    Test that unauthenticated users can access the list of resources.
    """
    client = APIClient()
    url = reverse('resource')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # Optionally add more assertions based on expected response data

@pytest.mark.django_db
def test_resource_update_unauthenticated():
    """
    Test that unauthenticated users cannot update a specific resource.
    """
    # Create a resource for testing
    resource = Resource.objects.create(title='Test Resource', author='Test Author')

    client = APIClient()
    url = reverse('detail-resource', args=[resource.pk])
    data = {'title': 'Updated Title'}
    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data
    assert response.data['detail'] == 'Authentication credentials were not provided.'

@pytest.mark.django_db
def test_resource_delete_unauthenticated():
    """
    Test that unauthenticated users cannot delete a specific resource.
    """
    # Create a resource for testing
    resource = Resource.objects.create(title='Test Resource', author='Test Author')

    client = APIClient()
    url = reverse('detail-resource', args=[resource.pk])
    response = client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data
    assert response.data['detail'] == 'Authentication credentials were not provided.'
