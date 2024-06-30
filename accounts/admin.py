from django.contrib import admin
from .models import User, OneTimePassword

class AcountAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name', 'email', 'date_joined')
admin.site.register(User, AcountAdmin)
admin.site.register(OneTimePassword)