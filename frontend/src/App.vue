<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-2 mb-3">
            Music App Client
        </div>
        <div class="mb-3">
            <u>Song List</u>:             
        </div>
        <pre>{{ response_data }}</pre>

        <!-- Song Cards -->
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            <div class="col" v-for="song in songs" :key="song.id">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">{{ song.title }}</h5>
                        <p class="card-text">
                            <strong>Artist:</strong> {{ song.artist.name }}<br>
                            <strong>Album:</strong> {{ song.album.title }}
                        </p>
                        <div class="d-flex justify-content-end">
                            <button class="btn btn-sm btn-warning me-2" @click="editSong(song)">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger" @click="deleteSong(song.id)">
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal for adding/editing songs -->
        <div class="modal fade" id="songModal" tabindex="-1">
            <!-- Modal content remains the same as before -->
        </div>

        <!-- Buttons for CRUD operations -->
        <div class="d-flex justify-content-end mb-3">
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#songModal">
                Add Song
            </button>
        </div>
    </div>
  </template>
  
<script>
export default {
    data() {
        return {
            response_data: '',
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/api/test.json')
        this.response_data = await response.json()
    }
}
</script>
