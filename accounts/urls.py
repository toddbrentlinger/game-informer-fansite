from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.CustomUserListView.as_view(), name='customuser-list'),
    path('<int:pk>/', views.CustomUserDetailView.as_view(), name='customuser-detail'),
    re_path(r'(?P<slug>[-\w]+)/$', views.customuser_detail_slug_view, name='customuser-detail-slug')
]