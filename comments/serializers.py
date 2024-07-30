from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from accounts.serializers import UserPublicSerializer
from resources.models import Resource

class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(source='user', read_only=True)
    resource_id = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all(), source='resource')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'resource_id', 'created_at', 'updated_at']

