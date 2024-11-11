<template>
    <div class="modal fade" id="addAlbumModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add Album</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetForm"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createAlbum">
                        <div class="mb-3">
                            <label for="albumTitle" class="form-label">Album Title</label>
                            <input type="text" class="form-control" id="albumTitle" v-model="albumTitle" required>
                        </div>
                        <div class="mb-3">
                            <label for="artistSelect" class="form-label">Artist</label>
                            <select class="form-select" id="artistSelect" v-model="currentArtist" required>
                                <option v-for="artist in artists" :key="artist.artist_id" :value="artist">
                                    {{ artist.artist_name }}
                                </option>
                            </select>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" @click="createAlbum">Add Album</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetForm">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        artists: Array
    },
    data() {
        return {
            albumTitle: '',
            currentArtist: null,
        };
    },
    methods: {
        // Resets the form information
        resetForm() {
            this.albumTitle = '';
            this.currentArtist = null;  
        },

        // Adds artist to list of albums
        async createAlbum() {
            const createUrl = `http://localhost:8000/api/albums/create/`;
            const data = {
                album_title: this.albumTitle,
                artist: this.currentArtist.artist_id  
            };

            try {
                const response = await fetch(createUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0],
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    this.$emit('album-added'); 
                    window.location.reload()
                    this.resetForm(); 
                } else {
                    console.error('Failed to add album');
                }
            } catch (error) {
                console.error('Error adding album:', error);
            }
        }
    }
}
</script>