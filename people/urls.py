from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.PersonListView.as_view(), name='people'),
    path('', views.person_list_view, name='people'),
    # path('<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),
    path('<int:pk>/', views.person_detail_view, name='person-detail'),
    re_path(r'(?P<slug>[-\w]+)/$', views.person_detail_slug_view, name='person-detail-slug'),
]