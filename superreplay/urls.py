from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.SuperReplayListView.as_view(), name='super-replay'),
    # path('<uuid:pk>/', views.SuperReplayDetailView.as_view(), name='super-replay-detail'),
    path('<uuid:pk>/', views.super_replay_detail_view, name='super-replay-detail'),
    re_path(r'(?P<slug>[-\w]+)/$', views.super_replay_detail_slug_view, name='super-replay-detail-slug'),
]
