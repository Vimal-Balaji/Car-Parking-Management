<template>
    <div class="row">
        <div class="col text-end">
            <button @click="logout" class="btn btn-danger m-3">Logout</button>
        </div>
    </div>
    
    <div class="container mt-3">
        <h1 class="text-center"> Location Details</h1>
        <form>
            <div class="row mb-3">
                <label class="col-sm-3 col-form-label" for="location">Location</label>
                <div class="col-sm-9">
                    <input v-model="location" type="text" id="location" class="form-control" placeholder="Enter location" />
                </div>
            </div>

            <div class="row mb-3">
            <label class="col-sm-3 col-form-label" for="address">Address</label>
            <div class="col-sm-9">
                <input v-model="address" type="text" id="address" class="form-control" placeholder="Enter address" />
            </div>
            
            </div>
            <div class="row mb-3">
            <label class="col-sm-3 col-form-label" for="pincode">Pin Code</label>
            <div class="col-sm-9">
                <input v-model="pincode" type="text" id="pincode" class="form-control" placeholder="Enter pincode" />
            </div>
            </div>
        </form>
        <div class="text-center" v-html="msg"></div>
        <div class="text-center">
            <button @click="addLocation" class="btn btn-primary fade-button">Add Location</button>
            
        </div>
</div>

</template>
<script>
import logoutMixin from '@/mixin/logoutMixin.js'
export default{
    mixins:[logoutMixin],
    data(){
        return{
            location:'',msg:'',
            address:'',
            pincode:'',
            isAdmin:false,
        }
    },
    methods:{
        async addLocation(){
            try {
                const res = await fetch('http://localhost:5000/api/location', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        location: this.location,
                        address: this.address,
                        pincode: this.pincode,
                       
                    })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.msg);
                this.msg = 'Location added successfully<br>Redirecting in 2 seconds...';
                setTimeout(() => {
                    this.$router.back();
                }, 2000); 
            } catch (err) {
                this.msg = err.msg || 'Failed to add location.';
            }
        }
    },
    async mounted()
    {
        this.isAdmin = localStorage.getItem("isAdmin") === "true";
        if(this.isAdmin === false)
        {
            this.$router.push({ name:'login' })
        }
        await this.fetchDashboard();
    }
}
</script>
<style scoped>
.container {
  max-width: 400px;
}

.fade-button {
  transition: background-color 0.3s ease;
}

/* Scoped hover fix using ::v-deep */
::v-deep(.fade-button:hover) {
  background-color: rgb(80, 43, 45) !important;
}
</style>

