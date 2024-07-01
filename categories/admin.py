from django.contrib import admin
from .models import Category
# Register your models here.\
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')

admin.site.register(Category, CategoryAdmin)