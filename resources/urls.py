from django.urls import path

from .import views

urlpatterns = [
    path('',views.ResourceMixinListView.as_view(), name = "resource"),
    path('<int:pk>/', views.ResourceMixinDetailView.as_view(), name ="detail-resource")
]