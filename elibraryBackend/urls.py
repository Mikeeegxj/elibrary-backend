
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from elibraryBackend.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path('api/v1/auth/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 