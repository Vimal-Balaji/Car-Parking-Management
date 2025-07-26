<template>
  <!-- Edit Location Modal -->
            <div class="modal fade" id="editLocationModal" tabindex="-1" aria-labelledby="editLocationModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">

                  <div class="modal-header">
                    <h5 class="modal-title" id="editLocationModalLabel">Edit Location</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>

                  <div class="modal-body">
                    <input type="text" class="form-control mb-3" v-model="editForm.location" placeholder="Enter new location" />
                    <input type="text" class="form-control mb-3" v-model="editForm.address" placeholder="Enter new address" />
                    <input type="text" class="form-control" v-model="editForm.pincode" placeholder="Enter new pincode" />
                  </div>
                  <div class="text-center">{{ modalMsg }}</div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" @click="EditLocation">Save Changes</button>
                  </div>

                </div>
              </div>
            </div>
        <!-- End Modal -->
</template>
<script>
export default {
  name: 'EditLocationModal',
  data() {
    return {
      editForm: {
        location: '',
        address: '',
        pincode: ''
      },

    }
  },
  methods:{
    open() {
      const modalEl = new bootstrap.Modal(this.$refs.modalRef);
      modalEl.show();
    },
    async EditLocation() {
    if (!this.selectedLoc) {
      alert('Please select a location to edit.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/location/${this.selectedLoc}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.editForm)
      });
      const result = await response.json();
      this.modalMsg = result.message || 'Location updated successfully';
      setTimeout(() => window.location.reload(), 1000);
    } catch (err) {
      console.error('Error updating location:', err);
      this.msg = 'Failed to update location';
    }
  },
  }
}
</script>