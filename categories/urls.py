from django.urls import path

from .import views

urlpatterns = [
    path('',views.CategoryMixinListView.as_view(), name = "category"),
    path('<int:pk>/', views.CategoryMixinDetailView.as_view(), name="category-detail")
]