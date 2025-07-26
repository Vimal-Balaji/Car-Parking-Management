<template>
    <div  class="container my-4 " style ="max-width: 1200px;">
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
        <div v-if="field=='location'" class="mb-4">
            <div class="mb-4">
                <label for="decision" class="form-label ml-3">Occupied/Not Occupied:</label>
                <select v-model="OccOrNot" id="decision" @change="fetchDetails" class="form-select w-50 text-center">
                    <option disabled value="">-- Choose a location --</option>
                    <option value=2>All Slots</option>
                    <option value=0>Not Occupied</option>
                    <option value=1>Occupied</option>
                </select>
            </div>
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
        <div v-else-if="field=='lotId'" class="mb-4">
            <label for="lotId" class="form-label ml-3">Choose LotId</label>
            <select v-model="spec" id="location" @change="fetchDetails" class="form-select w-50 text-center">
                <option disabled value="">-- Choose a lot ID --</option>
                <option value="all">All Lots</option>
                <option v-for="lot in lots" :key="lot.lotId" :value="lot.lotId">
                {{ lot.lotId }}-{{ lot.location }}
                </option>
            </select>
            <div class="mb-4">
                <label for="decision" class="form-label ml-3">Occupied/Not Occupied:</label>
                <select v-model="OccOrNot" id="decision" @change="fetchDetails" class="form-select w-50 text-center">
                    <option disabled value="">-- Choose a location --</option>
                    <option value=2>All Slots</option>
                    <option value=0>Not Occupied</option>
                    <option value=1>Occupied</option>
                </select>
            </div>

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
        <div v-else-if="field=='userId'" class="mb-4">
            <label for="userId" class="form-label ml-3">Choose userId</label>
            <select v-model="spec" id="userId" @change="fetchDetails" class="form-select w-50 text-center">
                <option disabled value="">-- Choose a user ID --</option>
                <option value="all">All users</option>
                <option v-for="user in users" :key="user.userId" :value="user.userId">
                {{ user.userId }}-{{ user.name }}
                </option>
            </select>
            <div v-if="details.length>0">
                <h2 class="text-center m-3">Filter based on User ID {{ spec }}</h2>
                <table class="table table-borderless m-3">
                    
                    <thead>
                        <th>S.no</th><th>user ID</th><th>Name</th><th>Email</th><th>Lot ID</th><th>Slot No.</th><th>Vehicle no</th><th>Start date</th><th>End date</th><th>Price</th>
                    </thead>
                    <tbody>
                        <tr v-for="(detail,index) in details" :key="index">
                            <td>{{index+1}}</td><td>{{ detail.userId }}</td><td>{{detail.userName}}</td><td>{{ detail.email }}</td><td>{{detail.lotId}}</td><td>{{ detail.slotId}}</td><td>{{ detail.vehicleNo }}</td><td>{{ detail.startTime }}</td><td>{{ detail.endTime }}</td><td>{{ detail.price }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                not foundd
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
            users:[],
        }
    },
    methods:
    {
        
        async fetchDetails()
        {
            this.details=[];
            const response=await this.request(`/api/gets/${this.OccOrNot}/${this.field}/${this.spec}`);
            this.details=response;
            
        }
    },
    async mounted()
    {
    
            const response = await this.request('/api/location');
            this.locations = response.location || [];
            const lotResponse = await this.request('/api/lot');
            this.lots = lotResponse.lotList || [];
            const userResponse = await this.request('/api/users');
            this.users = userResponse || [];

    }
}
</script>