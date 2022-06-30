from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='games'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    path('platforms/', views.PlatformListView.as_view(), name='platforms'),
    path('developers/', views.DeveloperListView.as_view(), name='developers'),
    re_path(r'(?P<stub>[-\w]+)/$', views.game_detail_slug_view, name='game-detail-slug'),

    path('platforms/<int:pk>/', views.PlatformDetailView.as_view(), name='platform-detail'),
    re_path(r'platforms/(?P<stub>[-\w]+)/$', views.platform_detail_slug_view, name='platform-detail-slug'),

    path('developers/<int:pk>/', views.DeveloperDetailView.as_view(), name='developer-detail'),
    re_path(r'developers/(?P<stub>[-\w]+)/$', views.developer_detail_slug_view, name='developer-detail-slug')
]