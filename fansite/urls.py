from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('replay/', views.ReplayEpisodeListView.as_view(), name='replay'),
    path('replay/<uuid:pk>/', views.ReplayEpisodeDetailView.as_view(), name='replay-detail'),
    path('replay/s<int:season>/<int:number>/', views.ReplayEpisodeDetailView.as_view()),
]