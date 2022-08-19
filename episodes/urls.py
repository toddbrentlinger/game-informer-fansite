from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.episode_list_view, name='episodes'),
    path('<int:pk>/', views.EpisodeDetailView.as_view(), name='episode-detail'),
    re_path(r'(?P<slug>[-\w]+)/$', views.episode_detail_slug_view, name='episode-detail-slug'),
]
