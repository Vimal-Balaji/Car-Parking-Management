<template>
    <div  class="container my-4 " style ="max-width: 800px;">
        <h1 class="text-center">Admin Dashboard</h1>
        <nav class="nav-bar d-flex justify-content-center gap-4 my-3">
        <router-link to="/admin" class="nav-link">Home</router-link>
        <router-link to="/admin/users" class="nav-link">Users</router-link>
        <router-link to="/admin/search" class="nav-link">Search</router-link>
        <router-link to="/admin/charts" class="nav-link">Charts</router-link>
        </nav>
        <div class="d-flex justify-content-end">
        <button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="logout"><span>Log Out</span></button>
        </div>
        <div class="mb-4">
            <label for="option" class="form-label ml-3">Choose field to be Filtered</label>
            <select v-model="field" id="option" class="form-select w-50 text-center">
                <option disabled value="">-- Choose a field --</option>
                <option value="location">Location</option>
                <option value="lotId">Lot ID</option>
                <option value="userId">user ID</option>
            </select>
        </div>
        <div v-if="field==='location' || field==='lotId'" class="mb-4">
            <label for="OccOrNot" class="form-label ml-3">Occupied/Not Occupied:</label>
            <select v-model="OccOrNot" id="OccOrNot" @change="fetchDetails" class="form-select w-50 text-center">
                <option disabled value="">-- Choose a location --</option>
                <option value=2>All Slots</option>
                <option value=0>Not Occupied</option>
                <option value=1>Occupied</option>
            </select>
        </div>
        <div v-if="field=='location'" class="mb-4">
            <label for="location" class="form-label ml-3">Choose Location</label>
            <select v-model="spec" id="location" @change="fetchDetails" class="form-select w-50 text-center">
                <option disabled value="">-- Choose a location --</option>
                <option value="all">All Locations</option>
                <option v-for="loc in locations" :key="loc" :value="loc">
                {{ loc }}
                </option>
            </select>
            <div v-if="details.length>0">
                <h2 class="text-center m-3">Filter based on {{ spec }} location</h2>
                <table class="table table-borderless m-3">
                    
                    <thead>
                        <th>S.no</th><th>Location</th><th>Lot ID</th><th>Slot No.</th><th>Occupied</th>
                    </thead>
                    <tbody>
                        <tr v-for="(detail,index) in details" :key="index">
                            <td>{{index+1}}</td><td>{{ detail.location }}</td><td>{{detail.lotId}}</td><td>{{ detail.slotId}}</td><td>{{ detail.isOccupied }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else >
                <h3 class="text-center  mt-3"><strong>The details doesnot exist</strong></h3>
            </div>
        </div>
        <div v-if="field=='lotId'" class="mb-4">
            <label for="lotId" class="form-label ml-3">Choose LotId</label>
            <select v-model="spec" id="lotId" @change="fetchDetails" class="form-select w-50 text-center">
                <option disabled value="">-- Choose a lot ID --</option>
                <option v-for="lot in lots" :key="lot.lotId" :value="lot.lotId">
                    {{lot.lotId}}-{{lot.location}}
                </option>
            </select>
            <div v-if="details.length>0">
                <h2 class="text-center m-3">Filter based on Lot ID {{ spec }}</h2>
                <table class="table table-borderless m-3">
                    
                    <thead>
                        <th>S.no</th><th>Location</th><th>Lot ID</th><th>Slot No.</th><th>Occupied</th>
                    </thead>
                    <tbody>
                        <tr v-for="(detail,index) in details" :key="index">
                            <td>{{index+1}}</td><td>{{ detail.location }}</td><td>{{detail.lotId}}</td><td>{{ detail.slotId}}</td><td>{{ detail.isOccupied }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else >
                <h3 class="text-center  mt-3"><strong>The details doesnot exist</strong></h3>
            </div>
        </div>
        <div v-if="field=='userId'" class="mb-4">
            <label for="userId" class="form-label ml-3">Enter User ID</label>
            <select v-model="spec" id="userId" @change="fetchDetails" class="form-select w-50 text-center">
                <option disabled value="">-- Choose a user ID --</option>
                <option value="all">All user-Id</option>
                <option v-for="user in userList" :key="user.userId" :value="user.userId">
                    {{user.userId}}-{{user.name}}
                </option>
            </select>
            <div v-if="details.length>0">
                <h2 class="text-center m-3">Filter based on User ID {{ spec }}</h2>
                <table class="table table-borderless m-3">
                    
                    <th>S.no</th><th>user ID</th><th>User Name</th><th>Lot ID</th><th>Slot No.</th><th>Vehicle No.</th><th>Start Time</th><th>End Time</th>
                    <tbody>
                        <tr v-for="(detail,index) in details" :key="index">
                            <td>{{index+1}}</td><td>{{ detail.userId}}</td><td>{{ detail.userName}}</td><td>{{ detail.lotId }}</td><td>{{detail.slotId}}</td><td>{{ detail.vehicleNo }}</td><td>{{ detail.startTime}}</td><td>{{ detail.endTime}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else >
                <h3 class="text-center  mt-3"><strong>The details doesnot exist</strong></h3>
            </div>
        </div>
    </div>
</template>
<script>
import logoutMixin from '@/mixin/logoutMixin.js'
import authMixin from '@/mixin/authMixin.js'
export default{
    mixins:[logoutMixin,authMixin],
    data()
    {
        return {
            OccOrNot:2,
            field:"",
            spec:"",
            locations:[],
            details:[],
            lots:[],
            userList:[],
        }
    },
    methods:
    {
        
        async fetchDetails()
        {
            const response=await this.request(`/api/gets/${this.OccOrNot}/${this.field}/${this.spec}`);
            this.details=response;
            console.log(this.details)
        }
    },
    async mounted()
    {
    
            const response = await this.request('/api/location');
            this.locations = response.location || [];
            const lotResponse = await this.request('/api/lot');
            this.lots = lotResponse.lotList || [];
            const userResponse = await this.request('/api/users');
            this.userList = userResponse || [];

    }
}
</script>