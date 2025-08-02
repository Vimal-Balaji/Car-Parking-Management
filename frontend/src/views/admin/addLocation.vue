<template>
  <div class="container my-3">
    <h1 class="text-center">Location Details</h1>

    <div class="d-flex justify-content-between mb-4">
      <!-- Back Button -->
      <button class="btn btn-dark d-flex align-items-center gap-2 px-3 py-1 " @click="goBack">
        <span>Back</span>
      </button>

      <!-- Logout Button -->
      <button class="btn btn-dark d-flex align-items-center gap-2 px-3 py-1 " @click="logout">
        <span>Log Out</span>
      </button>
    </div>

    <form>
      <div class="row mb-3">
        <label class="col-4 text-end col-form-label" for="location">Location</label>
        <div class="col-8">
          <input v-model="location" type="text" id="location" class="form-control w-75 " placeholder="---Enter location---" />
        </div>
      </div>

      <div class="row mb-3">
        <label class="col-4 text-end col-form-label" for="address">Address</label>
        <div class="col-8">
          <input v-model="address" type="text" id="address" class="form-control w-75 " placeholder="---Enter address---" />
        </div>
      </div>

      <div class="row mb-3">
        <label class="col-4 text-end col-form-label" for="pincode">Pin Code</label>
        <div class="col-8">
          <input v-model="pincode" type="text" id="pincode" class="form-control w-75" placeholder="---Enter pincode---" />
        </div>
      </div>

      <div class="row mb-3">
        <label class="col-4 text-end col-form-label" for="maxSlot">Max Slot</label>
        <div class="col-8">
          <input v-model="maxSlot" type="text" id="maxSlot" class="form-control w-75" placeholder="---Enter maxSlot---" />
        </div>
      </div>

      <div class="row mb-3">
        <label class="col-4 text-end col-form-label" for="price">Price</label>
        <div class="col-8">
          <input v-model="price" type="text" id="price" class="form-control w-75" placeholder="---Enter price---" />
        </div>
      </div>
    </form>

    <div class="text-center" >{{ msg }}</div>

    <div class="text-center">
      <button @click="addLocation" class="btn btn-dark">Add Location</button>
    </div>
  </div>
</template>

<script>
import logoutMixin from '@/mixin/logoutMixin.js'
import authMixin from '@/mixin/authMixin.js'
export default{
    mixins:[logoutMixin,authMixin],
    data(){
        return{
            location:'',msg:'',lotId:'',
            address:'',
            pincode:'',
            maxSlot:'',
            price:'',
            isAdmin:false,
        }
    },
    methods:{
        async addLocation(){
            try {
                const token = localStorage.getItem('token');
                const response=await this.request('http://localhost:5000/api/location',"POST",{'location':this.location,'address':this.address,'pincode':this.pincode,'price':this.price,'maxSlot':this.maxSlot})
                this.msg = `${response.message}    Redirecting in 2 seconds...`;
                const res=await this.request(`http://localhost:5000/api/sendMail`,"POST",{"choice":"createLot","price":this.price,"location":this.location,"lotId":response.lotId,"maxSlots":this.maxSlots})
                setTimeout(() => {
                    this.$router.back();
                }, 2000); 
            } catch (err) {
                this.msg = err.msg || 'Failed to add location.';
            }
        },
        goBack() {
    this.$router.back(); // Go to previous page
  },
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
  max-width: 600px;
}


</style>

