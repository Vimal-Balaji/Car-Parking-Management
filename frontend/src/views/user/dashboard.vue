<template>
  <div class="container my-4">
    <h1 class="text-center">DashBoard</h1>
    <nav class="nav-bar d-flex justify-content-center gap-4 my-3">
      <router-link to="/dashboard" class="nav-link">Home</router-link>
      <router-link to="/dashboard/book" class="nav-link">Booked </router-link>
      <router-link to="/dashboard/charts" class="nav-link">Charts</router-link>
      <router-link to="/dashboard/profile" class="nav-link">Profile</router-link>
    </nav>
    <div class="d-flex justify-content-end mb-3">
      <button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="logout">
        <span>Log Out</span>
      </button>
    </div>
    <div class="d-flex justify-content-center">
      <div class="text-center">
        <div v-if="message">{{ message }}</div>
        <div v-else>Loading...</div>
      </div>
    </div>
    <div class="mb-4">
      <label for="location" class="form-label ml-3">Select Location:</label>
      <select v-model="selectedLoc" id="location" @change="fetchSlots" class="form-select w-50 text-center">
        <option disabled value="">-- Choose a location --</option>
        <option v-for="loc in locations" :key="loc" :value="loc">
          {{ loc }}
        </option>
      </select>
      <div v-if="selectedLoc == ''" class="text mt-5 fs-5 fw-medium">
  <p>Please select a location to view available slots.</p>
  <p>Click on the Book Slot button near the lotId to book a slot.</p>
  <p>The slots are available for booking only if the lot is not full.</p>
  <p>Only the lots can be selected; the slots are filled in ascending order.</p>
</div>
      <div v-if="Object.keys(slotDict).length > 0">
        {{ AvlMsg }}
        <h2 class="text-center mt-3">Available Slots</h2>
        <div v-for="(slots, lot) in slotDict" :key="lot" class="mb-4 p-3 border rounded bg-light">
          <h4 class="mt-3">{{ lot }}:</h4>
          <button class="btn" data-bs-toggle="modal" data-bs-target="#bookSlotModal" @click="assignLot(lot, slotDetails[lot][2])">Book Slot</button>
        <p class="d-flex mb-3">Available Slots:{{ slotDetails[lot][0] }}/{{ slotDetails[lot][1] }}&nbsp;&nbsp;&nbsp;Price:{{ slotDetails[lot][2] }}</p>
        <div class="d-flex flex-wrap justify-content-start gap-2">
        <button v-for="(slot, index) in slots" :key="index" class="slot-button btn" :class="slot[1] ? 'btn-danger' : 'btn-success'" data-bs-toggle="modal" data-bs-target="#SlotModal" >{{ slot[0] }}</button>
        </div>
      </div>
    </div>   
   </div>
  </div>
  <!-- book Slot Modal -->
  <div class="modal fade" id="bookSlotModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Book Parking Slot</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p><strong>Lot:</strong> {{ bookSlot.lotId }}</p>
          <p><strong>Price:</strong> {{ bookSlot.price }}</p>
           <input type="text" class="form-control mb-3" v-model="bookSlot.vehicleNo" placeholder="Enter vehicle no" />
           
           <label for="startDate">Date:</label>
           <input type="date" id="startDate" name="StartDate" v-model="bookSlot.startDate" class="form-control mb-3">
           <label for="startTime">Time:</label>
           <input type="time" id="startTime" name="startTime" v-model="bookSlot.startTime" class="form-control mb-3">
            
           <label for="endDate">Date:</label>
           <input type="date" id="endDate" name="endDate" v-model="bookSlot.endDate" class="form-control mb-3">
           <label for="endTime">Time:</label>
           <input type="time" id="endTime" name="endTime" v-model="bookSlot.endTime" class="form-control mb-3">
           
                    
        </div>
        <div class="text-center mb-3"><strong>{{ modalMsg }}</strong></div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="confirmBooking">Confirm Booking</button>
          
        </div>
      </div>
    </div>
  </div>
  <!-- End Modal -->

</template>


<script>
import logoutMixin from '@/mixin/logoutMixin.js'
import authMixin from '@/mixin/authMixin.js'
export default {
  name: 'dashboard',
  mixins: [logoutMixin, authMixin],
  data() {
    return {
      message: '',
      modalMsg:'' ,     // starts empty
      isAdmin: false,
      name:'',
      locations:[],
      selectedLoc:"",
      slotDict: {},
      slotDetails: {},
      bookSlot: {
        lotId:"",
        price:"",
        vehicleNo: "",
        startDate: "",
        endDate: "",
        startTime:"",
        endTime:"",
      },
    }
  },
  methods:{
    async fetchSlots() {
    try {
      const response = await fetch(`http://localhost:5000/api/slots/${this.selectedLoc}`);
      const data = await response.json();
      this.slotDict = data[0]; // lotSlots
      this.slotDetails = data[1]; // lotDetails (optional if used
    } catch (error) {
      console.error('Error fetching slots:', error);
      this.msg = 'Error fetching slots';
    }
},
     async assignLot(lotId, price) {
    this.bookSlot.lotId = lotId;
    this.bookSlot.price = price; // Assuming price is at index 2
    this.modalMsg = `Booking ${lotId} for Rs.${price}`;
    },
    async confirmBooking() {
      try{
        const response=await this.request(`http://localhost:5000/api/book`,"POST",this.bookSlot);
        this.modalMsg = response.message;
        if (response.success) {
          setTimeout(() => window.location.reload(), 1000);
        }
        
      }
      catch (error) {
        console.error('Error confirming booking:', error);
        this.modalMsg = 'Error confirming booking';
      }
    },
},
  async mounted() {
    this.isAdmin = localStorage.getItem("isAdmin") === "true"
    const data=await this.request('http://localhost:5000/api/users');
    this.message = data.message;
    this.name=localStorage.getItem("name")
    const response = await this.request('/api/location');
    this.locations = response.location || [];
    await this.fetchDashboard()  
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
