<template>
  <div class="container my-5">
    <h1 class="text-center">Profile</h1>

    <nav class="nav-bar d-flex justify-content-center gap-4 my-3">
      <router-link to="/dashboard" class="nav-link">Home</router-link>
      <router-link to="/dashboard/book" class="nav-link">Booked</router-link>
      <router-link to="/dashboard/charts" class="nav-link">Charts</router-link>
      <router-link to="/dashboard/profile" class="nav-link">Profile</router-link>
    </nav>
    <div class="d-flex justify-content-end">
            <button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="logout">
            <span>Log Out</span></button>
    </div>
    <!-- View Profile -->
    <div v-if="editProfile" class="modal-body mt-3">
            <div class="row mb-2">
                <div class="col-4 text-end fw-bold">User ID&nbsp;&nbsp;:</div>
                <div class="col-sm-8">{{ details.userId }}</div>
            </div>
            <div class="row mb-2">
                <div class="col-4 text-end fw-bold">Email&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:</div>
                <div class="col-8">{{ details.email }}</div>
            </div>    
            <div class="row mb-2">
                <div class="col-4 text-end fw-bold">Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:</div>
                <div class="col-8">{{ details.name }}</div>
            </div>
            
            <div class="row mb-2">
                <div class="col-4 text-end fw-bold">Address:</div>
                <div class="col-8">{{ details.address }}</div>
            </div>
        <div class="d-flex justify-content-center mt-3"><button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="toggleEdit">Edit Profile</button></div>
    </div>

    <!-- Edit Profile -->
    <div v-else class="modal-body text center mt-3">
        <div class="row mb-2">
            <div class="col-4 text-end fw-bold">User ID&nbsp;&nbsp;:</div>
            <div class="col-sm-8">{{ details.userId }}</div>
        </div>
        <div class="row mb-2">
            <div class="col-4 text-end fw-bold">Email&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:</div>
            <div class="col-8">{{ details.email }}</div>
        </div>
        <div class="d-flex flex-column align-items-center">
            <input type="text" class="form-control w-50 mb-3" v-model.trim="details.name" placeholder="Enter your name"/>
            <input type="text" class="form-control w-50 mb-3" v-model.trim="details.address" placeholder="Enter your address"/>
        </div>
        <div class="d-flex justify-content-center mt-3"><button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="updateProfile">Update Profile</button></div>
    </div>

    <div class="text-center mt-3">{{ message }}</div>
  </div>
</template>

<script>
import logoutMixin from '@/mixin/logoutMixin.js';
import authMixin from '@/mixin/authMixin.js';

export default {
  mixins: [logoutMixin, authMixin],
  data() {
    return {
      message: '',
      editProfile: true,
      details: {
        userId: localStorage.getItem('userId'),
        name: '',
        address: '',
        email: '',
      },
    };
  },
  methods: {
    toggleEdit() {
      this.editProfile = !this.editProfile;
    },
    
    async updateProfile() {
      console.log('hello from Update profiel')
      const response = await this.request('/api/users', 'PUT', this.details);
      this.message = response.message;
      setTimeout(() => window.location.reload(), 1000);
    },
  },
  async mounted() {
    const response = await this.request(`/api/users/${this.details.userId}`);
    this.details.name = response.name;
    this.details.email = response.email;
    this.details.address = response.address;
  },
};
</script>

<style>
.container {
  max-width: 800px;
}
</style>
