from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('<int:id>/update/', views.post_update, name='post_update'),
    path('<int:id>/delete/', views.post_delete, name='post_delete'),
    path('create/', views.create_post, name='post_create'),
]