<template>
  <div class="container my-5" style="max-width: 500px;">
    <h2 class="text-center mb-4">Sign Up</h2>

    <div class="mb-3">
      <label class="form-label">Name</label>
      <input type="text" v-model="name" class="form-control" placeholder="Enter name" />
    </div>

    <div class="mb-3">
      <label class="form-label">Email</label>
      <input type="email" v-model="email" class="form-control" placeholder="Enter email" />
    </div>

    <div class="mb-3">
      <label class="form-label">Password</label>
      <input type="password" v-model="password" class="form-control" placeholder="Enter password" />
    </div>

    <div class="text-center">
      <button @click="signup" class="btn btn-dark rounded-pill px-4">Sign Up</button>
    </div>

    <p v-if="message" class="mt-3 text-center text-danger">{{ message }}</p>
  </div>
</template>
<script>
   export default{
    data() {
    return {
      email: '',
      password: '',
      name:'',
      message: ''
    };
  },
  methods: {
    
    async signup() {
      try {
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
            {this.$router.push('/login');}
        else 
            {this.message=`${data.message}`;}
      } catch (err) {
        this.message = `${err.message}`;
      }
    }
  }
   } 
</script>