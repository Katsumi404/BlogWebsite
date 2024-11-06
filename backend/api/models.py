from django.db import models

# Create your models here.
class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)  
    artist_name = models.CharField(max_length=128)  

    def __str__(self):
        return self.artist_name  

class Album(models.Model):
    album_id = models.AutoField(primary_key=True)  
    album_title = models.CharField(max_length=128)  
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  

    def __str__(self):
        return self.album_title  

class Song(models.Model):
    song_id = models.AutoField(primary_key=True)  
    song_title = models.CharField(max_length=128)  
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  
    album = models.ForeignKey(Album, on_delete=models.CASCADE)  

    def __str__(self):
        return self.song_title  