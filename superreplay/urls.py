from django.urls import path, re_path
from . import views

# TODO:
# super-replay/bloodborne
# super-replay/bloodborne/5
# super-replay/bloodborne-episode-5
urlpatterns = [
    path('', views.SuperReplayListView.as_view(), name='super-replay'),
    # path('<int:pk>/', views.SuperReplayDetailView.as_view(), name='super-replay-detail'),
    path('<int:pk>/', views.super_replay_detail_view, name='super-replay-detail'),
    re_path(r'(?P<slug>[-\w]+)/$', views.super_replay_detail_slug_view, name='super-replay-detail-slug'),
    re_path(r'(?P<slug>[-\w]+)/(?P<num>[0-9]+)/$', views.super_replay_episode_detail_slug_view, name='super-replay-episode-detail-slug'),
]
