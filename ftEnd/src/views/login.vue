<template>
  <div class="container mt-5">
    <h3>Login</h3>
    <div class="form-group mt-3">
      <label>Email</label>
      <input v-model="email" type="email" class="form-control" placeholder="Enter email" />
    </div>
    <div class="form-group mt-3">
      <label>Password</label>
      <input v-model="password" type="password" class="form-control" placeholder="Enter password" />
    </div>
    <button @click="login" class="btn btn-primary mt-4">Login</button>
    <p class="mt-3">
      Don't have an account?
      <router-link to="/signup">Sign Up</router-link>
    </p>
    <p v-if="message" class="text-danger mt-3">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      message: ''
    }
  },
  methods: {
    async login() {
  try {
    const res = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: this.email, password: this.password })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message)

    // Store token and user data
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('isAdmin', data.user.isAdmin)
    localStorage.setItem('userId', data.user.userId)
    localStorage.setItem('name', data.user.name)

    // Debug logging
    console.log('Login successful, isAdmin:', data.user.isAdmin)
    
    // Redirect based on role
    if (data.user.isAdmin) {
      console.log('Redirecting to admin')
      this.$router.push({ name: 'admin' }) // Ensure this matches router config
    } else {
      console.log('Redirecting to dashboard')
      this.$router.push({ name: 'dashboard' }) // Ensure this matches router config
    }
    
  } catch (err) {
    console.error('Login failed:', err)
    this.message = err.message || 'Login failed.'
  }
}
  }
}
</script>

<style scoped>
.container {
  max-width: 400px;
}
</style>
