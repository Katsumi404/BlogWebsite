<template>
    <div class="container pt-3">
      <div class="h1 text-center border rounded bg-light p-2 mb-3">Song List</div>
  
      <!-- Add Song Button triggers AddSongModal -->
      <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSongModal">Add Song</button>
  
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
    </div>
  </template>
  
  <script>
  import AddSongModal from './components/AddSongModal.vue';
  import EditSongModal from './components/EditSongModal.vue';
  
  export default {
    components: {
      AddSongModal,
      EditSongModal
    },
    data() {
      return {
        songs: [],
        artists: [],
        albums: [],
        selectedSong: null, // This will store the song being edited
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
        this.selectedSong = { ...song }; // Copy song data to avoid mutation
      },
  
      // Method to fetch songs after adding or updating a song
      async fetchSongs() {
        await this.fetchData(); // Re-fetch data to update the song list
        this.selectedSong = null; // Reset selected song after editing
      }
    }
  };
  </script>