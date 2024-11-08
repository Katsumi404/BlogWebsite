from django.shortcuts import render
from django.http import JsonResponse
from .models import Artist, Album, Song


def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })

def fetch_artists(request):
    artists = Artist.objects.all()
    # Convert the data to a list of dictionaries for JSON compatibility
    artists_data = [{"artist_id": artist.artist_id, "artist_name": artist.artist_name} for artist in artists]
    return JsonResponse({'artists': artists_data})

def fetch_albums(request):
    albums = Album.objects.all()
    # Convert each album to a dictionary
    albums_data = [{"album_id": album.album_id, "album_title": album.album_title, "artist_id": album.artist.artist_id} for album in albums]
    return JsonResponse({'albums': albums_data})

def fetch_songs(request):
    songs = Song.objects.all()
    # Convert each song to a dictionary, including related artist and album IDs
    songs_data = [{"song_id": song.song_id, "song_title": song.song_title, "artist_id": song.artist.artist_id, "album_id": song.album.album_id} for song in songs]
    return JsonResponse({'songs': songs_data})