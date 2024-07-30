from django.urls import path

from .import views

urlpatterns = [
    path('',views.CommentMixinListView.as_view(), name = "comment"),
    path('<int:pk>/', views.CommentMixinDetailView.as_view(), name='comment-detail')
]