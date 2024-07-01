from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

