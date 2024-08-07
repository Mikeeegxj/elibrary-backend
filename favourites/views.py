from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from .models import Favourite
from resources.models import Resource
from rest_framework.response import Response  # Add this import
from .serializers import FavouriteSerializer
from django.shortcuts import get_object_or_404

class FavouriteListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class FavouriteDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def get_object(self):
        resource_id = self.request.query_params.get('resource_id')
        return get_object_or_404(Favourite, user=self.request.user, resource_id=resource_id)
