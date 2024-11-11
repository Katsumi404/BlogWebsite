<template>
    <div class="container pt-3">
        <!-- Website header -->
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Music App Client
        </div>
        <div class="mb-3 ">
            <u>Song List</u>:             
        </div>

        <!-- Button to open song modal -->
        <div class="d-flex justify-content-end mb-3">
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSongModal" @click="prepareAddForm()">
                Add Song
            </button>
        </div>

        <!-- Song Cards -->
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            <div class="col" v-for="song in songs" :key="song.song_id">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">{{ song.song_title }}</h5>
                        <p class="card-text">
                            <strong>Artist:</strong> {{ song.artist.artist_name }}<br>
                            <strong>Album:</strong> {{ song.album.album_title }}
                        </p>
                        <div class="d-flex justify-content-end">
                            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editSongModal" @click="setCurrentInfo(song,song.album,song.artist); filterAlbums()">
                                Edit
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal for editing songs -->
        <div class="modal fade" id="editSongModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Edit Song</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="update_song">
                            <div v-if="currentSong" class="mb-3">
                                <label for="songTitle" class="form-label">Song Title</label>
                                <input 
                                    type="text" 
                                    class="form-control" 
                                    id="songTitle"
                                    v-model="currentSong.song_title"
                                    required
                                >
                            </div>
                            <div v-if="currentArtist" class="mb-3">
                                <label for="artistSelect" class="form-label">Artist</label>
                                <select 
                                    class="form-select" 
                                    id="artistSelect"
                                    @change="filterAlbums"
                                    v-model="currentSong.artist.artist_id"
                                    required
                                >
                                    <option v-for="artist in artists" 
                                            :key="artist.artist_id" 
                                            :value="artist.artist_id">
                                        {{ artist.artist_name }}
                                    </option>
                                </select>
                            </div>
                            <div v-if="currentAlbum" class="mb-3">
                                <label for="albumSelect" class="form-label">Album</label>
                                <select 
                                    class="form-select" 
                                    id="albumSelect"
                                    v-model="currentSong.album.album_id"
                                    required
                                >
                                    <option v-for="album in filteredAlbums" 
                                            :key="album.album_id" 
                                            :value="album.album_id">
                                        {{ album.album_title }}
                                    </option>
                                </select>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-primary" @click="update_song()">
                            Save Changes
                        </button>
                        <button class="btn btn-danger" @click="delete_song()">
                            Delete
                        </button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="removeCurrentInfo">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal for adding songs -->
        <div class="modal fade" id="addSongModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Add Song</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="create_song">
                            <div v-if="currentSong" class="mb-3">
                                <label for="songTitle" class="form-label">Song Title</label>
                                <input 
                                    type="text" 
                                    class="form-control" 
                                    id="songTitle"
                                    v-model="currentSong.song_title"
                                    required
                                >
                            </div>
                            <div v-if="currentArtist" class="mb-3">
                                <label for="artistSelect" class="form-label">Artist</label>
                                <select 
                                    class="form-select" 
                                    id="artistSelect"
                                    @change="filterAlbums"
                                    v-model="currentSong.artist.artist_id"
                                    required
                                >
                                    <option v-for="artist in artists" 
                                            :key="artist.artist_id" 
                                            :value="artist.artist_id">
                                        {{ artist.artist_name }}
                                    </option>
                                </select>
                            </div>
                            <div v-if="currentAlbum" class="mb-3">
                                <label for="albumSelect" class="form-label">Album</label>
                                <select 
                                    class="form-select" 
                                    id="albumSelect"
                                    v-model="currentSong.album.album_id"
                                    required
                                >
                                    <option v-for="album in filteredAlbums" 
                                            :key="album.album_id" 
                                            :value="album.album_id">
                                        {{ album.album_title }}
                                    </option>
                                </select>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-primary" @click="create_song()">
                            Add song
                        </button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="removeCurrentInfo">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </template>
  

<script>
export default {
    
    data() {
        return {
            songs: [],
            albums: [],
            artists: [],
            filteredAlbums: [],
            currentSong: null, 
            currentArtist: null, 
            currentAlbum: null
        }
    },
    async mounted() {
        try {
            // Use Promise.all to fetch all endpoints concurrently
            const [songsResponse, albumsResponse, artistsResponse] = await Promise.all([
                fetch('http://localhost:8000/api/songs/'),
                fetch('http://localhost:8000/api/albums/'),
                fetch('http://localhost:8000/api/artists/')
            ]);
            const [songsData, albumsData, artistsData] = await Promise.all([
                songsResponse.json(),
                albumsResponse.json(),
                artistsResponse.json()
            ]);
            this.songs = songsData;
            this.albums = albumsData;
            this.artists = artistsData;
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    },
    methods: {
        // Set the currentSong, currentAlbum, and currentArtist to the selected song
        setCurrentInfo(song, album, artist) {
            this.currentSong = { ...song };
            this.currentAlbum = { ...album};
            this.currentArtist = { ...artist};
        },
        // Reset the currentSong, currentAlbum, and currentArtist to null
        removeCurrentInfo() {
            this.currentSong = null;
            this.currentAlbum = null;
            this.currentArtist = null;
            this.filteredAlbums =  [];
        },
        filterAlbums() {
            if (this.currentArtist) {
                this.filteredAlbums = this.albums.filter(album => album.artist.artist_id === this.currentArtist.artist_id);
            } else {
                this.filteredAlbums = [];
            }
        },
        prepareAddForm() {
            this.currentSong = {
                song_title: '',
                artist: {
                    artist_id: null 
                },
                album: {
                    album_id: null 
                }
            };
            this.currentArtist = this.artists.length > 0 ? this.artists[0] : null;
            if (this.currentArtist) {
                this.filterAlbums(); 
                this.currentAlbum = this.filteredAlbums.length > 0 ? this.filteredAlbums[0] : null;
            }
        },


        // Makes the custom path for a song and deletes it with fetch API
        async delete_song() {
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
                    // Remove the song from the local list
                    this.songs = this.songs.filter(song => song.song_id !== this.currentSong.song_id);
                    console.log('Song deleted successfully');
                } else {
                    console.error('Failed to delete song');
                }
            } catch (error) {
                console.error('Error deleting song:', error);
            }
        },
        async update_song() {
            const updateUrl = `http://localhost:8000/api/songs/update/${this.currentSong.song_id}/`; 
            const updatedData = {
                song_title: this.currentSong.song_title,  
                artist: this.currentArtist.artist_id,          
                album: this.currentAlbum.album_id             
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
                    const updatedSong = await response.json();
                    const index = this.songs.findIndex(song => song.song_id === this.currentSong.song_id);
                    if (index !== -1) {
                        this.songs.splice(index, 1, updatedSong);
                    }
                } else {
                    console.error('Failed to update song');
                }
            } catch (error) {
                console.error('Error updating song:', error);
            }
        },
        async create_song() {
            const createUrl = `http://localhost:8000/api/songs/create/`;
            const updatedData = {
                song_title: this.currentSong.song_title,
                artist: this.currentArtist.artist_id,
                album: this.currentAlbum.album_id
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
                    const responseData = await response.json();
                    console.log('Song added successfully:', responseData);
                    
                    window.location.reload();
                } else {
                    // Handle failure: Show error message or something went wrong
                    const errorData = await response.json();
                    console.error('Error adding song:', errorData.error);
                    alert('Failed to add song: ' + errorData.error);
                }
            } catch (error) {
                console.error('Error adding song:', error);
                alert('Something went wrong while adding the song.');
            }
        },
    }
}
</script>
