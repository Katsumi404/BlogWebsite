"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
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
from .views import test_api_view, fetch_artists, fetch_albums, fetch_songs
from django.urls import path, include

# Django admin login details:
#  user: admin
#  password: Cloud*8f

urlpatterns = [
    # API entry points should be defined here
    path('test.json', test_api_view, name='api_test'),
    path('songs.json', fetch_songs, name='songs'),
    path('artists.json', fetch_artists, name='artist'),
    path('albums.json', fetch_albums, name='albums'),
    path('admin/', admin.site.urls),
]
