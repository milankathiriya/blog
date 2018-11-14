from django.urls import path
from . import views


urlpatterns = [
    # path('', views.homeapi),
    path('', views.PostListView.as_view()),
    path('create/', views.PostCreateView.as_view()),
    path('<int:pk>/', views.PostRetrieveView.as_view()),
    path('<int:pk>/update/', views.PostUpdateView.as_view()),
    path('<int:pk>/delete/', views.PostDeleteView.as_view()),
    # path('<int:pk>/', views.PostDetailView.as_view()),
]