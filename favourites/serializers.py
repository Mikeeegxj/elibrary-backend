# serializers.py
from rest_framework import serializers
from .models import Favourite
from resources.models import Resource

class FavouriteSerializer(serializers.ModelSerializer):
    resource_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favourite
        fields = ['id', 'user', 'resource', 'resource_id', 'created_at']
        read_only_fields = ['user', 'resource']

    def create(self, validated_data):
        resource_id = validated_data.pop('resource_id')
        resource = Resource.objects.get(id=resource_id)
        user = self.context['request'].user  # Ensure to get the user from the request context
        return Favourite.objects.create(user=user, resource=resource, **validated_data)
