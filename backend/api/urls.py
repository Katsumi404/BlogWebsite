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
from .views import test_api_view, get_songs, get_albums, get_artists, delete_song, update_song, create_song
from django.urls import path, include

# Django admin login details:
#  user: admin
#  password: Cloud*8f

urlpatterns = [
    # API entry points should be defined here
    path('test.json', test_api_view, name='api_test'),
    path('songs/', get_songs, name='get_songs'),
    path('albums/', get_albums, name='get_albums'),
    path('artists/', get_artists, name='get_artists'),
    path('songs/delete/<int:song_id>/', delete_song, name='delete_song'),
    path('songs/update/<int:song_id>/', update_song, name='update_song'),
    path('songs/create/', create_song, name='create_song'),
    path('admin/', admin.site.urls),
]
