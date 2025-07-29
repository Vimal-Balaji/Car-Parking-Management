<template>
  <div class="about-page container mt-5">
    <div class="row">
      <div class="col-lg-12">
        <h1 class="text-center mb-4">About Our Parking Management System</h1>
        <div class="d-flex justify-content-end mb-3">
      <button class="btn btn-dark rounded-pill d-flex align-items-center gap-2 px-4 py-2" @click="logout">
    <span>Log In/Sign Up</span></button>
    </div>
        <div class="card shadow mb-5">
          <div class="card-body">
            <h2 class="card-title">Project Overview</h2>
            <p class="card-text">
              Our Parking Management System is a comprehensive solution designed to modernize and streamline parking operations.
              Whether for commercial parking lots, municipal street parking, or private facilities, our system provides
              real-time monitoring, efficient space utilization, and enhanced user experience.
            </p>
          </div>
        </div>

        <div class="row features mb-5">
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <i class="fas fa-car fa-3x text-primary mb-3"></i>
                <h3 class="card-title">Real-time Monitoring</h3>
                <p class="card-text">
                  Track parking space availability in real-time with our advanced sensor technology and intuitive dashboard.
                </p>
              </div>
            </div>
          </div>
          
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <i class="fas fa-mobile-alt fa-3x text-success mb-3"></i>
                <h3 class="card-title">Mobile Integration</h3>
                <p class="card-text">
                  Users can find, reserve, and pay for parking spots directly from their smartphones with our mobile app.
                </p>
              </div>
            </div>
          </div>
          
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <div class="card-body">
                <i class="fas fa-chart-line fa-3x text-info mb-3"></i>
                <h3 class="card-title">Analytics & Reporting</h3>
                <p class="card-text">
                  Gain valuable insights with comprehensive reports on parking usage, revenue, and peak times.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="row mb-5">
          <div class="col-lg-6">
            <div class="card">
              <div class="card-header bg-dark text-white">
                <h3 class="mb-0">Our Technology</h3>
              </div>
              <div class="card-body">
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">
                    <i class="fas fa-check-circle text-success mr-2"></i>
                    IoT sensors for accurate space detection
                  </li>
                  <li class="list-group-item">
                    <i class="fas fa-check-circle text-success mr-2"></i>
                    Cloud-based data processing
                  </li>
                  <li class="list-group-item">
                    <i class="fas fa-check-circle text-success mr-2"></i>
                    Machine learning for demand prediction
                  </li>
                  <li class="list-group-item">
                    <i class="fas fa-check-circle text-success mr-2"></i>
                    Secure payment processing
                  </li>
                </ul>
              </div>
            </div>
          </div>
          
          <div class="col-lg-6">
            <div class="card">
              <div class="card-header bg-secondary text-white">
                <h3 class="mb-0">Benefits</h3>
              </div>
              <div class="card-body">
                <div class="media mb-3">
                  <i class="fas fa-dollar-sign fa-2x text-success mr-3"></i>
                  <div class="media-body">
                    <h5 class="mt-0">Increased Revenue</h5>
                    Optimized space utilization leads to higher occupancy rates and revenue.
                  </div>
                </div>
                <div class="media mb-3">
                  <i class="fas fa-users fa-2x text-info mr-3"></i>
                  <div class="media-body">
                    <h5 class="mt-0">Improved Customer Experience</h5>
                    Reduced search time and convenient payment options enhance user satisfaction.
                  </div>
                </div>
                <div class="media">
                  <i class="fas fa-tree fa-2x text-primary mr-3"></i>
                  <div class="media-body">
                    <h5 class="mt-0">Environmental Impact</h5>
                    Less circling means reduced emissions and fuel consumption.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

       

        <div class="contact-cta text-center py-4 bg-light rounded">
          <h3 class="mb-3">Ready to transform your parking operations?</h3>
          <p class="lead mb-4">Contact us today to schedule a demo or learn more about our solutions.</p>
          <button class="btn btn-dark btn-lg">Contact Us</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
  metaInfo() {
    return {
      title: 'About - Parking Management System',
      meta: [
        { name: 'description', content: 'Learn about our Parking Management System and how it can optimize your parking operations.' }
      ]
    }
  },
  methods: {  
    logout() {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.about-page {
  padding-bottom: 50px;
}

.card {
  transition: transform 0.3s ease;
  border: none;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.features .card {
  text-align: center;
  padding: 20px;
}

.team-section .card {
  border: none;
  box-shadow: 0 2px 15px rgba(45, 41, 41, 0.1);
}

.contact-cta {
  background: linear-gradient(135deg, #888b8d 0%, #293542 100%);
  border: 1px solid #dee2e6;
}
</style>