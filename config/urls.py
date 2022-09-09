"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from fansite import views as fansite_views
from shows import views as shows_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('accounts.urls')),
    path('fansite/', include('fansite.urls')),
    path('', RedirectView.as_view(url='fansite/', permanent=True)),
    path('games/', include('games.urls')),
    path('people/', include('people.urls')),
    path('replay/', include('replay.urls')),
    path('super-replay/', include('superreplay.urls')),
    path('search/', fansite_views.search, name='search'),
    path('episodes/', include('episodes.urls')),
    path('shows/', shows_views.ShowListView.as_view(), name='shows'),
    re_path(r'(?P<show_slug>[-\w]+)/(?P<showepisode_slug>[-\w]+)/$', shows_views.showepisode_detail_slug_view, name='showepisode-detail-slug'),
    re_path(r'(?P<slug>[-\w]+)/', shows_views.show_detail_slug_view, name='show-detail-slug'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
