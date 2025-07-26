<template>
    <div>
        <h> Sign Up</h>
            <div><label>Name</label><input type="text" v-model="name" placeholder="Enter name"></div>
            <div><label>Email</label><input type="email" v-model="email" placeholder="Enter email"></div>
            <div><label>Password</label><input type="password" v-model="password" placeholder="Enter password"></div>
            <div><button @click="signup">Sign Up</button></div>
            <p v-if="message">{{ message }}</p>
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