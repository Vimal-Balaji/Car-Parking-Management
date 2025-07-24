<template>
  <div class="container mt-5">
    <h2>Dashboard</h2>

    <div v-if="message" class="alert alert-success mt-3">
      {{ message }}
    </div>
    <div v-else class="mt-3">Loading...</div>
    <div v-if="isAdmin === true" class="alert alert-info mt-3">
      You are logged in as an <strong>admin</strong>.
    </div>
    <div v-else class="alert alert-info mt-3">
      You are logged in as a <strong>regular user</strong>.
    </div>

    <button @click="logout" class="btn btn-danger mt-4">Logout</button>
  </div>
</template>

<script>
import logoutMixin from '@/mixin/logoutMixin.js'

export default {
  name: 'dashboard',
  mixins: [logoutMixin],
  data() {
    return {
      message: '',      // starts empty
      isAdmin: false
    }
  },
  async mounted() {
    this.isAdmin = localStorage.getItem("isAdmin") === "true"
    try {
        const { data } = await axios.get('http://localhost:5000/api/dashboard', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.message = data.message
      } catch (err) {
        console.error("Error:", err)
        localStorage.removeItem("token")
        this.$router.push({ name: 'login' })
      }
    await this.fetchDashboard()   // ← await so you can catch errors here if you want
  }
}
</script>
<style scoped>
.container {
  max-width: 600px;
}
</style>
