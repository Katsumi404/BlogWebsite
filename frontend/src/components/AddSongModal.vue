<template>
    <div class="modal fade" id="addSongModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add Song</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetForm"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="create_song">
                        <div class="mb-3">
                            <label for="songTitle" class="form-label">Song Title</label>
                            <input type="text" class="form-control" id="songTitle" v-model="currentSong.song_title" required>
                        </div>
                        <div class="mb-3">
                            <label for="artistSelect" class="form-label">Artist</label>
                            <select class="form-select" id="artistSelect" @change="filterAlbums" v-model="currentSong.artist.artist_id" required>
                                <option v-for="artist in artists" :key="artist.artist_id" :value="artist.artist_id">
                                    {{ artist.artist_name }}
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="albumSelect" class="form-label">Album</label>
                            <select class="form-select" id="albumSelect" v-model="currentSong.album.album_id" required>
                                <option v-for="album in filteredAlbums" :key="album.album_id" :value="album.album_id">
                                    {{ album.album_title }}
                                </option>
                            </select>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" @click="create_song">Add song</button>
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
        albums: Array
    },
    data() {
        return {
            currentSong: {
                song_title: '',
                artist: { artist_id: null },
                album: { album_id: null }
            },
            filteredAlbums: []
        }
    },
    
    methods: {
        filterAlbums() {
            if (this.currentSong.artist.artist_id) {
                this.filteredAlbums = this.albums.filter(album => album.artist.artist_id === this.currentSong.artist.artist_id);
            } else {
                this.filteredAlbums = [];
            }
        },

        resetForm() {
            this.currentSong = { song_title: '', artist: { artist_id: null }, album: { album_id: null } };
            this.filteredAlbums = [];
        },

        async create_song() {
            const createUrl = `http://localhost:8000/api/songs/create/`;
            const updatedData = {
                song_title: this.currentSong.song_title,
                artist: this.currentSong.artist.artist_id,
                album: this.currentSong.album.album_id
            };

            try {
                const response = await fetch(createUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0],
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify(updatedData)
                });
                if (response.ok) {
                    this.$emit('song-added'); // Emit event to parent when song is added
                    window.location.reload()
                } else {
                    console.error('Failed to add song');
                }
            } catch (error) {
                console.error('Error adding song:', error);
            }
        }
    }
}
</script>