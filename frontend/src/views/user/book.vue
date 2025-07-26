<template>
    <div class="container my-4" width>
        <h1 class="text-center">Booked Slots</h1>
        <nav class="nav-bar d-flex justify-content-center gap-4 my-3">
            <router-link to="/dashboard" class="nav-link">Home</router-link>
            <router-link to="/dashboard/book" class="nav-link">Booked </router-link>
            <router-link to="/dashboard/charts" class="nav-link">Charts</router-link>
            <router-link to="/dashboard/profile" class="nav-link">Profile</router-link>
        </nav>
        <div class="d-flex justify-content-end">
            <button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="logout">
            <span>Log Out</span></button>
        </div>
        <div><strong>{{ message }}</strong></div>
        <table class="table table-borderless m-3">
            <thead>
                <th class="text-center">S.no</th><th class="text-center">Location</th><th class="text-center">Lot ID</th><th class="text-center">Slot No.</th><th class="text-center">Vehicle No</th><th class="text-center">Start Time</th><th class="text-center">End Time</th><th class="text-center">Price</th><th class="text-center">Action</th>
            </thead>
            <tbody>
                <tr v-for="(detail,index) in bookDetails" :key="index">
                    <td>{{index+1}}</td><td>{{ detail.location }}</td><td>{{ detail.lotId }}</td><td>{{detail.slotId}}</td><td>{{ detail.vehicleNo }}</td><td>{{ detail.startTime }}</td><td>{{ detail.endTime }}</td><td>{{ detail.price }}</td><td><button class="btn " @click="releaseSlot(detail.slotId, detail.lotId)">Release</button></td>
                </tr>
            </tbody>
            
        </table>

    </div>
</template>
<script>
import logoutMixin from '@/mixin/logoutMixin.js'
import authMixin from '@/mixin/authMixin.js'
export default{
    mixins: [logoutMixin, authMixin],
    data(){
        return {
            message:"",
            bookDetails:[],
        }
    },
    methods:
    {
       async releaseSlot(slotId, lotId) {
        const response=await this.request('/api/book',"DELETE", { "lotId":lotId, "slotId":slotId });
        this.message=response.message || "Slot released successfully";
        setTimeout(() => window.location.reload(), 1000);
       }
        
    },
    async mounted(){
        this.message= "Loading booked slots..."
        try {
            const response = await this.request('/api/book');
            this.bookDetails =response.bookedDetails;
                console.log(this.bookDetails);
                this.message = " ";
        } catch (error) {
            console.error("Error fetching booked slots:", error);
            this.message = "Failed to load booked slots.";
        }
    }
}
</script>
<style>
.container {
  max-width: 800px;
}
</style>