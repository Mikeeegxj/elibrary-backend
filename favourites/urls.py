# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.FavouriteListCreateView.as_view(), name="favourite-list-create"),
    path('delete/', views.FavouriteDeleteView.as_view(), name="favourite-delete"),
]
