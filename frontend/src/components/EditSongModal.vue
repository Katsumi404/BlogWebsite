<template>
    <div class="modal fade" id="editSongModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Edit Song</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetForm"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateSong">
              <div class="mb-3">
                <label for="editSongTitle" class="form-label">Song Title</label>
                <input type="text" class="form-control" id="editSongTitle" v-model="currentSong.song_title" required>
              </div>
              <div class="mb-3">
                <label for="editArtistSelect" class="form-label">Artist</label>
                <select class="form-select" id="editArtistSelect" @change="filterAlbums" v-model="currentSong.artist.artist_id" required>
                  <option v-for="artist in artists" :key="artist.artist_id" :value="artist.artist_id">
                    {{ artist.artist_name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="editAlbumSelect" class="form-label">Album</label>
                <select class="form-select" id="editAlbumSelect" v-model="currentSong.album.album_id" required>
                  <option v-for="album in filteredAlbums" :key="album.album_id" :value="album.album_id">
                    {{ album.album_title }}
                  </option>
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="updateSong">Save changes</button>
            <button class="btn btn-danger" @click="deleteSong()">Delete</button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetForm">Close</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      artists: Array,
      albums: Array,
      songToEdit: Object
    },

    data() {
      return {
        currentSong: { song_title: '', artist: { artist_id: null }, album: { album_id: null } },
        filteredAlbums: []
      };
    },

    // Waits to see when artist changes so it can show the relevant albums
    watch: {
      songToEdit(newSong) {
        if (newSong) {
          this.currentSong = { ...newSong };
          this.filterAlbums();
        }
      }
    },

    methods: {
      // Filters all albums into a new (kinda since it's in data) array, where only the songs from the artist is
      filterAlbums() {
        if (this.currentSong.artist.artist_id) {
          this.filteredAlbums = this.albums.filter(album => album.artist.artist_id === this.currentSong.artist.artist_id);
        } else {
          this.filteredAlbums = [];
        }
      },

      //clears the form
      resetForm() {
        this.currentSong = { song_title: '', artist: { artist_id: null }, album: { album_id: null } };
        this.filteredAlbums = [];
      },

      // Changes the song information
      async updateSong() {
        const updateUrl = `http://localhost:8000/api/songs/update/${this.currentSong.song_id}/`;
        const updatedData = {
          song_title: this.currentSong.song_title,
          artist: this.currentSong.artist.artist_id,
          album: this.currentSong.album.album_id
        };
  
        try {
          const response = await fetch(updateUrl, {
            method: 'PUT',
            headers: {
              'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0],
              'Content-Type': 'application/json'
            },
            credentials: 'same-origin',
            body: JSON.stringify(updatedData)
          });
          if (response.ok) {
            this.$emit('song-updated'); 
            $('#editSongModal').modal('hide');
          } else {
            console.error('Failed to update song');
          }
        } catch (error) {
          console.error('Error updating song:', error);
        }
      },

      // Deletes the song using the song id
      async deleteSong() {
            const deleteUrl = `http://localhost:8000/api/songs/delete/${this.currentSong.song_id}/`;
            try {
                const response = await fetch(deleteUrl, { 
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0],
                        'Content-Type': 'application/json',
                    },
                    credentials: 'same-origin',
                });
                if (response.ok) {
                    window.location.reload()
                    console.log('Song deleted successfully');
                } else {
                    console.error('Failed to delete song');
                }
            } catch (error) {
                console.error('Error deleting song:', error);
            }
        },
    }
  }
  </script>