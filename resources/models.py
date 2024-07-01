from django.db import models
from django.conf import settings
from django.db.models import Q
from categories.models import Category

# Create your models here.
class Resource(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    image_file = models.ImageField(upload_to='images/', blank=True, default='images/default_blogbanner.jpg')
    file = models.FileField(upload_to='files/', blank=True, null=True)
    view_count = models.IntegerField(default=0)
    author = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
