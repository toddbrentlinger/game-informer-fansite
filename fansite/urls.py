from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/ajax/episodes', views.get_episodes, name='get_episodes'),
]
