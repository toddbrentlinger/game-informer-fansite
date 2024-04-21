from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.replay_episode_list_view, name='replay'),
    path('<int:pk>/', views.replay_episode_detail_view, name='replay-detail'),
    path('s<int:season>/<int:number>/', views.replay_episode_detail_season_episode_view, name='replay-detail-season-episode'),

    # Replay Segments
    path('segments/', views.segment_type_list_view, name='segments'),

    # Regex
    re_path(r'segments/(?P<slug>[-\w]+)/$', views.segment_type_detail_slug_view, name='segment-type-detail-slug'),
    re_path(r'(?P<slug>[-\w]+)/$', views.replay_episode_detail_slug_view, name='replay-detail-slug'),

    # AJAX
    path('get/ajax/random-replay-episode', views.get_random_replay_episode, name='get_random_replay_episode'),
]
