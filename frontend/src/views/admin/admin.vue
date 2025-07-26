<template>
  <div class="container my-4">
    <h1 class="text-center">Admin Dashboard</h1>
    <nav class="nav-bar d-flex justify-content-center gap-4 my-3">
  <router-link to="/admin" class="nav-link">Home</router-link>
  <router-link to="/admin/users" class="nav-link">Users</router-link>
  <router-link to="/admin/search" class="nav-link">Search</router-link>
  <router-link to="/admin/charts" class="nav-link">Charts</router-link>
</nav>
    <div class="d-flex justify-content-end">
      <button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="logout">
    <span>Log Out</span></button>
    </div>
    <p v-if="isAdmin" class="fw-semibold text-center">Welcome, Admin!</p>

    <div class="mb-4">
      <label for="location" class="form-label ml-3">Select Location:</label>
      <select v-model="selectedLoc" id="location" @change="fetchSlots" class="form-select w-50 text-center">
        <option disabled value="">-- Choose a location --</option>
        <option value="All locations">All Locations</option>
        <option v-for="loc in locations" :key="loc" :value="loc">
          {{ loc }}
        </option>
      </select>
    </div>
     
    <div v-if="Object.keys(slotDict).length > 0">
        <h2 class="text-center mt-3">Available Slots</h2>
        <div v-for="(slots, lot) in slotDict" :key="lot" class="mb-4 p-3 border rounded bg-light">
          <h4 class="mb-3">{{ lot }}:</h4> <button class="btn flex-fill" data-bs-toggle="modal" data-bs-target="#LotModal" @click="viewLot(lot)">View/Edit Lot</button>
          <button class="btn  flex-fill" @click="deleteLot(lot)">Delete Lot</button>

          <p class="d-flex mb-3">Available Slots:{{ slotDetails[lot][0] }}/{{ slotDetails[lot][1] }}</p>
          <div class="d-flex flex-wrap justify-content-start gap-2">
          <button v-for="(slot, index) in slots" :key="index" class="slot-button btn" :class="slot[1] ? 'btn-danger' : 'btn-success'" data-bs-toggle="modal" data-bs-target="#SlotModal"  @click="viewSlot(slot[0],lot)">{{ slot[0] }}</button>
        </div>
      </div>
    </div>
    
    <div v-if="selectedLoc !== ''" class="d-flex justify-content-between gap-3 m-3">
        <button @click="deleteLocation" class="btn  flex-fill">Delete Location</button>
        <button class="btn flex-fill" data-bs-toggle="modal" data-bs-target="#editLocationModal" @click="viewLocation">View/Edit Location</button>
        <button class="btn flex-fill" data-bs-toggle="modal" data-bs-target="#addLotModal">Add Lot</button>
    </div>
    <button @click="addLocation" class="btn btn-primary text-center">Add Location</button>
    <div class="text-center mt-3" v-if="msg">{{ msg }}</div>
  </div>
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
        <!-- Add Lot modal-->
         <div class="modal fade" id="addLotModal" tabindex="-1" aria-labelledby="addLotModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">

                  <div class="modal-header">
                    <h5 class="modal-title" id="addLotModalLabel">Add Lot</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>

                  <div class="modal-body">
                    <input type="text" class="form-control mb-3" v-model="addLot.location" placeholder="Enter the location" />
                    <input type="text" class="form-control mb-3" v-model="addLot.maxSlots" placeholder="Enter max slots" />
                    <input type="text" class="form-control mb-3" v-model="addLot.price" placeholder="Enter the price" />
                  </div>
                  <div class="text-center">{{ AddLotMsg }}</div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" @click="submitLot">Save Changes</button>
                  </div>

                </div>
              </div>
            </div>

         <!--End Modal-->
         <!-- View/Edit Lot Modal -->
         <div class="modal fade" id="LotModal" tabindex="-1" aria-labelledby="LotModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">

                  <div class="modal-header">
                    <h5 class="modal-title" id="LotModalLabel">Add Lot</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>

                  <div class="modal-body">
                    <p><strong>Lot ID:</strong> {{ Lot.lotId }}</p>
                    <input type="text" class="form-control mb-3" v-model="Lot.location" placeholder="Enter the location" />
                    <input type="text" class="form-control mb-3" v-model="Lot.maxSlots" placeholder="Enter max slots" />
                    <input type="text" class="form-control mb-3" v-model="Lot.price" placeholder="Enter the price" />
                  </div>
                  <div class="text-center">{{ LotMsg }}</div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" @click="editLot">Save Changes</button>
                  </div>

                </div>
              </div>
            </div>
            <!--End Modal-->
            <!-- View/Delete Slot Modal -->
            <div class="modal fade" id="SlotModal" tabindex="-1" aria-labelledby="SlotModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">

                  <div class="modal-header">
                    <h5 class="modal-title" id="SlotModalLabel">View Slot</h5>
                    <div>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="FALSE"></button>
                    </div>
                  </div>

                  <div class="modal-body">
                    <p><strong>Lot ID:</strong> {{ Slot.lotId }}</p>
                    <p><strong>Slot ID:</strong> {{ Slot.slotId }}</p>
                    <p><strong>Is Occupied:</strong>
                      <span v-if="!Slot.isOccupied">No</span>
                      <button v-else class="btn btn-danger btn-sm" @click="toggleButton">Yes</button>
                    </p></div>
                    <div v-if="show">
                      <p><strong>User ID:</strong> {{ Slot.userId }}</p>
                      <p><strong>Start Time:</strong> {{ Slot.startTime }}</p>
                      <p><strong>End Time:</strong> {{ Slot.endTime }}</p>
                      <p><strong>Vehicle No:</strong> {{ Slot.vehicleNo }}</p>
                      <p><strong>Price:</strong> {{ Slot.price }}</p>
                  </div>
                  <div class="text-center">{{ SlotMsg }}</div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="FALSE">Cancel</button>
                    <button type="button" class="btn btn-primary" @click="deleteSlot">Delete Slot</button>
                  </div>

            </div>
          </div>
        </div>
        <!--End Modal-->

</template>
<script>
import logoutMixin from '@/mixin/logoutMixin.js'
import authMixin from '@/mixin/authMixin.js'
export default {
  mixins: [logoutMixin, authMixin],
  data() {
    return {
      modalMsg: '',
      msg: '',
      AddLotMsg: '',
      LotMsg: '',
      SlotMsg: '',
  
    isAdmin: false,
    show:false,
    locations: [],
    selectedLoc: '',
    selectedLot: '',
    slotDict: {},
    slotDetails: {},
    editForm: {
      address: '',
      pincode: '',
      location:'',
    },
    addLot:{
      location:'',
      maxSlots:'',
      price:'',
    },
    Lot:{
      location:'',
      maxSlots:'',
      price:'',
      lotId:'',
    },
    Slot:{
      lotId:'',
      slotId:'',
      isOccupied:'',
      userId:'',
      startTime:'',
      endTime:'',
      vehicleNo:'',
      price:'',
    }
    }
  },
  methods:{
    FALSE()
    {
      this.show=false;
    },
    async toggleButton()
    {
      this.show=!this.show;
    },
    async deleteSlot() {
      if (!this.Slot.slotId || !this.Slot.lotId) {
        alert('Please select a slot to delete.');
        return;
      }
      try {
        const response = await this.request(`http://localhost:5000/api/slots/${this.Slot.lotId}/${this.Slot.slotId}`, 'DELETE');
        this.SlotMsg = response.message || 'Slot deleted successfully';
        setTimeout(() => window.location.reload(), 1000);
      } catch (err) {
        console.error('Error deleting slot:', err);
        this.SlotMsg = 'Failed to delete slot';
      }
    },
    async viewSlot(slotId, lotId) {
      this.Slot.lotId = lotId;
      this.Slot.slotId = slotId;
      if (!slotId || !lotId) {
        alert('Please select a slot to view/edit.');
        return;
      }
      try {
        const response = await this.request(`http://localhost:5000/api/slots/${lotId}/${slotId}`, 'GET');
        this.Slot.isOccupied = response.isOccupied;
        this.Slot.userId = response.userId;
        this.Slot.startTime = response.startTime;
        this.Slot.endTime = response.endTime;
        this.Slot.vehicleNo = response.vehicleNo;
        this.Slot.price = response.price;
      } catch (err) {
        console.error('Error fetching slot:', err);
        this.SlotMsg = 'Failed to fetch slot';
      }
    },
    async viewLot(selectedLotId) {
      this.selectedLot = selectedLotId;
      if (!selectedLotId) {
        alert('Please select a lot to view/edit .');
        return;
      }
      try {
        const response = await fetch(`http://localhost:5000/api/lot/${selectedLotId}`);
        const data = await response.json();
        this.Lot.location= data.location;
        this.Lot.maxSlots = data.maxSlots;
        this.Lot.price = data.price;
        this.Lot.lotId = data.lotId;
      } catch (err) {
        console.error('Error fetching lot:', err);
        this.LotMsg = 'Failed to fetch lot';
      }
    },
    async editLot() {
      if (!this.selectedLoc) {
        alert('Please select a location to edit the lot.');
        return;
      }

      try {
        const response = await this.request(`http://localhost:5000/api/lot/${this.selectedLot}`,'PUT',this.Lot);
        if (response.status == 404) {
          this.LotMsg="Location does not exist";return;
        }
        this.LotMsg=response.message;
        setTimeout(() => window.location.reload(), 1000);
      } catch (err) {
        console.error('Error updating lot:', err);
        this.LotMsg = response.message;
      }
    },
    async submitLot() {
      if (!this.selectedLoc) {
        alert('Please select a location to add a lot.');
        return;
      }

      try {
        const response = await this.request('/api/lot', 'POST', this.addLot);
  
        this.AddLotMsg = response.message || 'Lot added successfully';
        setTimeout(() => window.location.reload(), 1000);
      } catch (err) {
        console.error('Error adding lot:', err);
        this.AddLotMsg = 'Failed to add lot';
      }
    },  
    async deleteLot(selectedLotId) {
      if (!selectedLotId) {
        alert('Please select a lot to delete.');
        return;
      }
      try {
        const response = await this.request(`/api/lot/${selectedLotId}`, 'DELETE');
        this.msg = response.message || 'Lot deleted successfully';
        setTimeout(() => window.location.reload(), 1000);
      } catch (err) {
        console.error('Error deleting lot:', err);
        this.msg = 'Failed to delete lot';
      }
    },
    async viewLocation()
    {
      if (!this.selectedLoc) {
        alert('Please select a location to view/edit.');
        return;
      }
      try {
        const response = await fetch(`http://localhost:5000/api/location/${this.selectedLoc}`);
        const data = await response.json();
        this.editForm.location = data.location;
        this.editForm.address = data.address;
        this.editForm.pincode = data.pincode;
      } catch (err) {
        console.error('Error fetching location:', err);
        this.msg = 'Failed to fetch location';
      }
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
    async fetchSlots(){
      this.addLot.location = this.selectedLoc;
     try {
      const response = await fetch(`http://localhost:5000/api/slots/${this.selectedLoc}`);
      const data = await response.json();
      this.slotDict = data[0];
      this.slotDetails = data[1];
    } catch (error) {
      console.error('Error fetching slots:', error);
      this.msg = 'Error fetching slots';
    }
    },
    async addLocation(){
      this.$router.push({ name: 'addLocation' })
    },
    async deleteLocation(){
      if (this.selectedLoc === '') {
        alert('Please select a location to delete.');
        return;
      }
      try{
        const response =await this.request('/api/location/' + this.selectedLoc,'DELETE');
        this.msg = response.message || 'Location deleted successfully';
        setTimeout(() => window.location.reload(), 1000);
      }
      catch (error) {
        console.error('Error deleting location:', error);
        this.msg = 'Failed to delete location';
      }
    }
  },
  async mounted() {
    this.isAdmin = localStorage.getItem("isAdmin") === "true";
    if (!this.isAdmin) {
      this.$router.push('/login'); // Redirect if not admin
      return;
    }
    try {
    const response = await this.request('/api/location');
    this.locations = response.location || [];
    await this.fetchDashboard();
  } catch (error) {
    console.error('Initialization error:', error);
    if (error.message.includes('401')) {
      this.$router.push('/login');
    }
  }
    await this.fetchDashboard()   // ← await so you can catch errors here if you want
  }
}
</script>
<style scoped>
.container {
  max-width: 800px;
}

.slot-button {
  width: 50px;
  height: 50px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 8px;
  font-size: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.1s ease;
}

.slot-button:hover {
  transform: scale(1.05);
}
</style>
