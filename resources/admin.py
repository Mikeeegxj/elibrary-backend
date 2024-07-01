from django.contrib import admin
from .models import Resource
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','author', 'created_at', 'updated_at')
admin.site.register(Resource, ResourceAdmin)