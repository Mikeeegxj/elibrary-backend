from rest_framework import serializers
from .models import Category

class CategoryRelatedFieldSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'description': value.description
        }

    def to_internal_value(self, data):
        return data

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
        ]