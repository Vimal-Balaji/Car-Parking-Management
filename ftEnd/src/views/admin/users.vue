<template>
  <div class="container my-4" style ="max-width: 800px;">
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
    <div class="text-center my-4">
      <h2>User List</h2>
    <table class="table table-borderless m-3">
      <thead>
        <tr>
          <th>S.no</th>
          <th>User ID</th>
          <th>Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in userList" :key="user.userId">
          <td>{{ index + 1 }}</td>
          <td>{{ user.userId }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>
</template>

<script>
import logoutMixin from '@/mixin/logoutMixin.js'
import authMixin from '@/mixin/authMixin.js'
export default{
    mixins:[logoutMixin,authMixin],
    data() {
        return {
            userList:[],
            locations:[]
        }
    },
    async mounted()
    {
        const response = await this.request('http://localhost:5000/api/users');
        this.userList = response;
        
    }

}
</script>