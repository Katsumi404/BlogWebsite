<template>
    <div class="container pt-3">
      <div class="h1 text-center border rounded bg-light p-2 mb-3">Song List</div>
  
      <!-- Add Song/Album/Artist Buttons -->
      <div class="d-flex gap-2 mb-3">
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addArtistModal">Add Artist</button>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addAlbumModal">Add Album</button>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSongModal">Add Song</button>
      </div>
  
      <!-- Song List Table -->
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div class="col" v-for="song in songs" :key="song.song_id">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ song.song_title }}</h5>
              <p class="card-text">
                <strong>Artist:</strong> {{ song.artist.artist_name }}<br />
                <strong>Album:</strong> {{ song.album.album_title }}
              </p>
              <!-- Edit Button triggers EditSongModal -->
              <button 
                class="btn btn-warning" 
                :data-bs-toggle="'modal'" 
                :data-bs-target="'#editSongModal'" 
                @click="prepareEdit(song)">
                Edit
              </button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- AddSongModal Component -->
      <AddSongModal 
        :artists="artists" 
        :albums="albums"
        @song-added="fetchSongs" />
  
      <!-- EditSongModal Component -->
      <EditSongModal 
        :artists="artists"
        :albums="albums"
        :songToEdit="selectedSong"
        @song-updated="fetchSongs" />

      <!-- AddArtistModal Component -->
      <AddArtistModal 
        @artist-added="fetchArtists" />

      <!-- AddAlbumModal Component -->
      <AddAlbumModal 
        :artists="artists"
        @album-added="fetchAlbums" />
    </div>
  </template>
  
  <script>
  // Fetching Components from component folder
  import AddSongModal from './components/AddSongModal.vue';
  import AddAlbumModal from './components/AddAlbumModal.vue';
  import AddArtistModal from './components/AddArtistModal.vue';
  import EditSongModal from './components/EditSongModal.vue';
  
  export default {
    // Exporting Components
    components: {
      AddSongModal,
      AddAlbumModal,
      AddArtistModal,
      EditSongModal
    },

    data() {
      return {
        songs: [],
        artists: [],
        albums: [],
        selectedSong: null, 
      };
    },

    async mounted() {
      await this.fetchData();
    },

    methods: {
      // Fetch the songs, artists, and albums
      async fetchData() {
        try {
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
          console.error('Error fetching data:', error);
        }
      },
  
      // Prepare song data to be edited
      prepareEdit(song) {
        this.selectedSong = { ...song };
      },
  
      // Method to fetch songs after adding or updating a song
      async fetchSongs() {
        await this.fetchData(); 
        this.selectedSong = null; 
      },

      // Method to fetch artist after adding an artist
      async fetchArtists() {
        await this.fetchData(); 
      },

      // Method to fetch artist after adding an album
      async fetchAlbums() {
        await this.fetchData(); 
      }
    }
  };
  </script>