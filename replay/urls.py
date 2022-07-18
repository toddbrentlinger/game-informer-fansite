from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ReplayEpisodeListView.as_view(), name='replay'),
    # path('<uuid:pk>/', views.ReplayEpisodeDetailView.as_view(), name='replay-detail'),
    path('<uuid:pk>/', views.replay_episode_detail_view, name='replay-detail'),
    path('s<int:season>/<int:number>/', views.ReplayEpisodeDetailView.as_view()),

    # Replay Segments
    path('segments/', views.SegmentTypeListView.as_view(), name='segments'),
    path('segments/<int:pk>', views.SegmentTypeDetailView.as_view(), name='segment-type-detail'),

    # Regex
    re_path(r'segments/(?P<slug>[-\w]+)/$', views.segment_type_detail_slug_view, name='segment-type-detail-slug'),
    re_path(r'(?P<slug>[-\w]+)/$', views.replay_episode_detail_slug_view, name='replay-detail-slug'),
]