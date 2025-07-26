// src/mixin/logoutMixin.js
import axios from 'axios'

export default {
  methods: {
    async fetchDashboard() {
      const token = localStorage.getItem("token")
      if (!token) {
        this.$router.push({ name: 'login' })
        return
      }

      
    },
    logout() {
      localStorage.clear()
      this.$router.push({ name: 'login' })
    }
  }
}
