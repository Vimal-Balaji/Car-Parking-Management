<template>
  <div class="wrapper">
    <div class="title"><span>Signup Form</span></div>
    <form @submit.prevent="handleSignup">
      <div class="row">
        <i class="fas fa-user"></i>
        <input type="text" v-model="name" placeholder="Name" required />
      </div>
      <div class="row">
        <i class="fas fa-envelope"></i>
        <input type="email" v-model="email" placeholder="Email" required />
      </div>
      <div class="row">
        <i class="fas fa-lock"></i>
        <input type="password" v-model="password" placeholder="Password" required />
      </div>
      <div class="row">
        <i class="fas fa-lock"></i>
        <input type="password" v-model="confirmPassword" placeholder="Confirm Password" required />
      </div>
      <div class="row button">
      <button class="btn btn-dark" @click="signup"> Sign Up</button>
      </div>
      <div class="signup-link">Already have an account? <router-link to="/login">Login now</router-link></div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    
    async signup() {
      try {
        if (this.password !== this.confirmPassword) {
        alert("Passwords do not match");
        return;
      }
        const res = await fetch('http://localhost:5000/api/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            name:this.name
          })
        });

        const data = await res.json();
        const status=res.status;
        if (!res.ok) throw new Error(data.message);
        if(status===201)
            {
              this.message="User added successfully"
              this.$router.push('/login');}
        else 
            {this.message=`${data.message}`;}
      } catch (err) {
        this.message = `${err.message}`;
      }
    }
  }
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css');

.wrapper {
  width: 380px;
  background: #fff;
  padding: 40px 30px;
  border-radius: 10px;
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.2);
  margin: 100px auto;
}

.wrapper .title {
  font-size: 24px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 25px;
  color: #333;
}

.wrapper .row {
  position: relative;
  height: 45px;
  margin-bottom: 25px;
}

.wrapper .row i {
  position: absolute;
  width: 47px;
  height: 100%;
  background: #333;
  color: #fff;
  font-size: 18px;
  text-align: center;
  line-height: 45px;
  border-radius: 5px 0 0 5px;
}

.wrapper .row input {
  width: 100%;
  height: 100%;
  padding-left: 55px;
  border: none;
  outline: none;
  background: #f0f0f0;
  border-radius: 5px;
  font-size: 16px;
}

.wrapper .row.button input {
  background: #333;
  color: #fff;
  font-weight: 500;
  cursor: pointer;
  transition: 0.3s;
}

.wrapper .row.button input:hover {
  background: #444;
}

.signup-link {
  text-align: center;
  font-size: 14px;
  margin-top: 20px;
}

.signup-link a {
  color: #007bff;
  text-decoration: none;
}
.signup-link a:hover {
  text-decoration: underline;
}
</style>
