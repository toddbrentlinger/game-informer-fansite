from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Replay
    path('replay/', views.ReplayEpisodeListView.as_view(), name='replay'),
    # path('replay/<uuid:pk>/', views.ReplayEpisodeDetailView.as_view(), name='replay-detail'),
    path('replay/<uuid:pk>/', views.replay_episode_detail_view, name='replay-detail'),
    path('replay/s<int:season>/<int:number>/', views.ReplayEpisodeDetailView.as_view()),

    # Replay Segments
    path('replay/segments/', views.SegmentTypeListView.as_view(), name='segments'),
    path('replay/segments/<int:pk>', views.SegmentTypeDetailView.as_view(), name='segment-type-detail'),

    # Regex
    re_path(r'replay/segments/(?P<stub>[-\w]+)/$', views.segment_type_detail_slug_view, name='segment-type-detail-slug'),
    re_path(r'replay/(?P<stub>[-\w]+)/$', views.replay_episode_detail_slug_view, name='replay-detail-slug'),
]