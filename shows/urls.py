from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ShowListView.as_view(), name='shows'),
    path('<int:pk>/', views.ShowDetailView.as_view(), name='show-detail'),
    re_path(r'(?P<slug>[-\w]+)/$', views.show_detail_slug_view, name='show-detail-slug'),
]
