from django.test import TestCase
from .models import Artist, Album, Song

# Create your tests here.
class ArtistModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(artist_name='Test Artist')

    def test_artist_str(self):
        self.assertEqual(str(self.artist), 'Test Artist')


class AlbumModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(artist_name='Test Artist')  # Create an artist first
        self.album = Album.objects.create(album_title='Test Album', artist=self.artist)

    def test_album_artist(self):
        self.assertEqual(self.album.artist, self.artist)

    def test_album_str(self):
        self.assertEqual(str(self.album), 'Test Album')


class SongModelTest(TestCase):
    def setUp(self):
        self.artist = Artist.objects.create(artist_name='Test Artist')  # Create an artist first
        self.album = Album.objects.create(album_title='Test Album', artist=self.artist)
        self.song = Song.objects.create(song_title='Test Song', album=self.album, artist=self.artist)

    def test_song_album(self):
        self.assertEqual(self.song.album, self.album)

    def test_song_artist(self):
        self.assertEqual(self.song.artist, self.artist)

    def test_song_str(self):
        self.assertEqual(str(self.song), 'Test Song')