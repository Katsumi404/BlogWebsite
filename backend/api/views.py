from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Artist, Album, Song
import json


def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })

@require_http_methods(["GET"])
def get_songs(request):
    songs = Song.objects.all()
    song_list = []
    for song in songs:
        song_list.append({
            'song_id': song.song_id,
            'song_title': song.song_title,
            'artist': {
                'artist_id': song.artist.artist_id,
                'artist_name': song.artist.artist_name
            },
            'album': {
                'album_id': song.album.album_id,
                'album_title': song.album.album_title
            }
        })
    return JsonResponse(song_list, safe=False)

@require_http_methods(["GET"])
def get_artists(request):
    artists = Artist.objects.all()
    artist_list = []
    for artist in artists:
        artist_list.append({
            'artist_id': artist.artist_id,
            'artist_name': artist.artist_name
        })
    return JsonResponse(artist_list, safe=False)

@require_http_methods(["GET"])
def get_albums(request):
    albums = Album.objects.all()
    album_list = [] 
    for album in albums:
        album_list.append({
            'album_id': album.album_id,
            'album_title': album.album_title,
            'artist': {
                'artist_id': album.artist.artist_id,
                'artist_name': album.artist.artist_name
            }
        })
    return JsonResponse(album_list, safe=False)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_song(request, song_id):
    try:
        song = Song.objects.get(song_id=song_id)
        song.delete()
        return JsonResponse({'message': 'Song deleted successfully'})
    except Song.DoesNotExist:
        return JsonResponse({'error': 'Song not found'}, status=404)

@csrf_exempt
@require_http_methods(["PUT"])
def update_song(request, song_id):
    try:
        song = Song.objects.get(song_id=song_id)
        data = json.loads(request.body)

        song.song_title = data.get("song_title", song.song_title)
        song.artist.artist_id = data.get("artist", song.artist.artist_id)  
        song.album.album_id = data.get("album", song.album.album_id)  
        
        song.save()
        song.artist.save()
        song.album.save()

        return JsonResponse({
            'song_id': song.song_id,
            'song_title': song.song_title,
            'artist': {
                'artist_id': song.artist.artist_id,
                'artist_name': song.artist.artist_name
            },
            'album': {
                'album_id': song.album.album_id,
                'album_title': song.album.album_title
            }
        }, status=200)
    except Song.DoesNotExist:
        return JsonResponse({'error': 'Song not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
@require_http_methods(["POST"])
def create_song(request):
    try:
        data = json.loads(request.body)
        artist_id = data.get("artist")
        artist = Artist.objects.get(artist_id=artist_id)
        album_id = data.get("album")
        album = Album.objects.get(album_id=album_id)

        song = Song.objects.create(
            song_title=data.get("song_title"),  
            artist=artist,  
            album=album,    
        )

        return JsonResponse({
            'song_id': song.song_id,
            'song_title': song.song_title,
            'artist': {
                'artist_id': song.artist.artist_id,
                'artist_name': song.artist.artist_name
            },
            'album': {
                'album_id': song.album.album_id,
                'album_title': song.album.album_title
            }
        }, status=201)
    except Artist.DoesNotExist:
        return JsonResponse({'error': 'Artist not found'}, status=404)
    except Album.DoesNotExist:
        return JsonResponse({'error': 'Album not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)