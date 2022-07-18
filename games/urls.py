from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='games'),
    path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),

    path('platforms/', views.PlatformListView.as_view(), name='platforms'),
    path('developers/', views.DeveloperListView.as_view(), name='developers'),
    path('collections/', views.CollectionListView.as_view(), name='collections'),
    path('franchises/', views.FranchiseListView.as_view(), name='franchises'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('themes/', views.ThemeListView.as_view(), name='themes'),
    path('keywords/', views.KeywordListView.as_view(), name='keywords'),

    re_path(r'(?P<slug>[-\w]+)/$', views.game_detail_slug_view, name='game-detail-slug'),

    path('platforms/<int:pk>/', views.PlatformDetailView.as_view(), name='platform-detail'),
    re_path(r'platforms/(?P<slug>[-\w]+)/$', views.platform_detail_slug_view, name='platform-detail-slug'),

    path('developers/<int:pk>/', views.DeveloperDetailView.as_view(), name='developer-detail'),
    re_path(r'developers/(?P<slug>[-\w]+)/$', views.developer_detail_slug_view, name='developer-detail-slug'),

    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-detail'),
    re_path(r'collections/(?P<slug>[-\w]+)/$', views.collection_detail_slug_view, name='collection-detail-slug'),

    path('franchises/<int:pk>/', views.FranchiseDetailView.as_view(), name='franchise-detail'),
    re_path(r'franchises/(?P<slug>[-\w]+)/$', views.franchise_detail_slug_view, name='franchise-detail-slug'),

    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    re_path(r'genres/(?P<slug>[-\w]+)/$', views.genre_detail_slug_view, name='genre-detail-slug'),

    path('themes/<int:pk>/', views.ThemeDetailView.as_view(), name='theme-detail'),
    re_path(r'themes/(?P<slug>[-\w]+)/$', views.theme_detail_slug_view, name='theme-detail-slug'),

    path('keywords/<int:pk>/', views.KeywordDetailView.as_view(), name='keyword-detail'),
    re_path(r'keywords/(?P<slug>[-\w]+)/$', views.keyword_detail_slug_view, name='keyword-detail-slug'),
]