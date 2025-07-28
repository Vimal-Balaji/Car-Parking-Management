<!-- <template>
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
   <div class="d-flex  mt-4">
      <button class="btn btn-dark d-flex align-items-center gap-2 px-4 py-2 rounded-0" @click="login">
        <span>Log In</span>
      </button>
    </div>
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
</style> -->
<template>
  <div class="wrapper mt-4">
    <div class="title">Login Form</div>
    <form>
      <div class="field">
        <input type="text" v-model="email" required />
        <label>Email Address</label>
      </div>
      <div class="field">
        <input type="password" v-model="password" required />
        <label>Password</label>
      </div>
      <div class="field">
        <button type="button" class="btn btn-dark rounded-0 w-100" @click="login">Login</button>
      </div>
      <div class="field mt-3">
        <button type="button" class="btn btn-secondary rounded-0 w-100" @click="signUp" >
           Sign Up
        </button>
      </div>
    </form>
    <div class="text-center m-3">{{ message }}</div>
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
    async signUp()
    {
      this.$router.push({name:"signup"})
    },
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
<style>
@import url('https://fonts.googleapis.com/css?family=Poppins:400,500,600,700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

html, body {
  display: grid;
  height: 100%;
  width: 100%;
  place-items: center;
  background: #f2f2f2;
}

::selection {
  background: #4158d0;
  color: #fff;
}

.wrapper {
  width: 380px;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.1);
}

.wrapper .title {
  font-size: 35px;
  font-weight: 600;
  text-align: center;
  line-height: 100px;
  color: #fff;
  user-select: none;
  border-radius: 15px 15px 0 0;
  background: linear-gradient(-135deg, #2d292d, #737478);
}

.wrapper form {
  padding: 10px 30px 50px 30px;
}

.wrapper form .field {
  height: 50px;
  width: 100%;
  margin-top: 20px;
  position: relative;
}

.wrapper form .field input {
  height: 100%;
  width: 100%;
  outline: none;
  font-size: 17px;
  padding-left: 20px;
  border: 1px solid lightgrey;
  border-radius: 25px;
  transition: all 0.3s ease;
}

.wrapper form .field input:focus,
.wrapper form .field input:valid {
  border-color: #4158d0;
}

.wrapper form .field label {
  position: absolute;
  top: 50%;
  left: 20px;
  color: #999999;
  font-weight: 400;
  font-size: 17px;
  pointer-events: none;
  transform: translateY(-50%);
  transition: all 0.3s ease;
}

.wrapper form .field input:focus ~ label,
.wrapper form .field input:valid ~ label {
  top: 0%;
  font-size: 16px;
  color: #4158d0;
  background: #fff;
  transform: translateY(-50%);
}

form .signup-link {
  color: #262626;
  margin-top: 20px;
  text-align: center;
}

form .signup-link a {
  color: #4158d0;
  text-decoration: none;
}

form .signup-link a:hover {
  text-decoration: underline;
}

</style>