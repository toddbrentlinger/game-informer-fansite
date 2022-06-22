from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='games'),
    re_path(r'(?P<stub>[-\w]+)$', views.GameDetailView.as_view(), name='game-detail-slug'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
]