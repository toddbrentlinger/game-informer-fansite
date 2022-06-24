from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='games'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    re_path(r'(?P<stub>[-\w]+)/$', views.game_detail_slug_view, name='game-detail-slug'),
]