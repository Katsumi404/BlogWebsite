<template>
    <div class="modal fade" id="addArtistModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Add Artist</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetForm"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createArtist">
                        <div class="mb-3">
                            <label for="artistName" class="form-label">Artist Name</label>
                            <input type="text" class="form-control" id="artistName" v-model="artistName" required>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" @click="createArtist">Add Artist</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetForm">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            artistName: ''
        };
    },

    methods: {
        // Resets the form information
        resetForm() {
            this.artistName = '';
        },

        // Adds artist to list of artists
        async createArtist() {
            const createUrl = `http://localhost:8000/api/artists/create/`;
            const data = {
                artist_name: this.artistName, 
            };

            try {
                const response = await fetch(createUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.cookie.split('csrftoken=')[1].split(';')[0],
                        'Content-Type': 'application/json',
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify(data),
                });
                if (response.ok) {
                    this.$emit('artist-added');
                    this.resetForm();
                } else {
                    const responseBody = await response.json();
                    console.error(`Failed to add artist. Status: ${response.status}, Response:`, responseBody);
                }
            } catch (error) {
                console.error('Error adding artist:', error);
            }
        }
    }
}
</script>