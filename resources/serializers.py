from rest_framework import serializers
from .models import Resource
from categories.models import Category
from accounts.serializers import UserPublicSerializer
from categories.serializers import CategoryRelatedFieldSerializer

class ResourceSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer('user', read_only=True)
    category = CategoryRelatedFieldSerializer(queryset=Category.objects.all())
    class Meta:
        model = Resource
        fields = [
            'id',
            'title',
            'content',
            'view_count',
            'image_file',
            'file',
            'category',
            'user',
            'author',
            'created_at',
            'updated_at',
        ]