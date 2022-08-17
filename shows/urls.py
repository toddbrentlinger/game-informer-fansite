from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ShowListView.as_view(), name='shows'),
    path('<int:pk>/', views.ShowDetailView.as_view(), name='show-detail'),
    re_path(r'(?P<slug>[-\w]+)/$', views.show_detail_slug_view, name='show-detail-slug'),
    path('episodes/', views.episode_list_view, name='episodes'),
    path('episodes/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode-detail'),
    re_path(r'episodes/(?P<slug>[-\w]+)/$', views.episode_detail_slug_view, name='episode-detail-slug'),
]
