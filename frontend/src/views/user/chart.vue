<template>
  <div class="container my-4">
    <h1 class="text-center">Slot Statistics</h1>

    <!-- Navigation -->
    <nav class="nav-bar d-flex justify-content-center gap-4 my-3">
      <router-link to="/dashboard" class="nav-link">Home</router-link>
      <router-link to="/dashboard/book" class="nav-link">Booked</router-link>
      <router-link to="/dashboard/charts" class="nav-link">Charts</router-link>
      <router-link to="/dashboard/profile" class="nav-link">Profile</router-link>
    </nav>

    <!-- Logout Button -->
    <div class="d-flex justify-content-end mb-3">
      <button class="btn btn-dark rounded-pill px-4 py-2" @click="logout">Log Out</button>
    </div>

    <!-- Chart Selector -->
    <div class="d-flex justify-content-center mb-4">
      <select v-model="selectedChart" class="form-select w-auto">
        <option value="bar">Bar Chart</option>
        <option value="pie">Pie Chart</option>
      </select>
    </div>

    <!-- Chart Display -->
    <div style="display: flex; justify-content: center; height: 70vh;">
      <div style="width: 700px; height: 500px;">
        <Bar v-if="selectedChart === 'bar'" :data="barChartData" :options="barChartOptions" />
        <Pie v-else :data="pieChartData" :options="pieChartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { Bar, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, ArcElement, CategoryScale, LinearScale
} from 'chart.js'

// Register chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale)

const selectedChart = ref('bar') // default to bar chart
const barChartData = ref({ labels: [], datasets: [] })
const pieChartData = ref({ labels: [], datasets: [] })

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Occupied vs Non-Occupied Slots by Location' }
  }
}

const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'bottom' },
    title: { display: true, text: 'Total Occupancy Overview (All Locations)' }
  }
}

// Vue Router instance
const router = useRouter()

// Logout function
function logout() {
  localStorage.clear()
  router.push({ name: 'login' }) // Make sure 'login' route has a defined name in your router
}

// Fetch chart data from backend
onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/slotStats/user')
    const data = res.data

    // Bar chart
    barChartData.value = {
      labels: data.bar_chart.map(item => item.location),
      datasets: [
        {
          label: 'Occupied Slots',
          backgroundColor: '#f87171',
          data: data.bar_chart.map(item => item.occupied)
        },
        {
          label: 'Non-Occupied Slots',
          backgroundColor: '#60a5fa',
          data: data.bar_chart.map(item => item.non_occupied)
        }
      ]
    }

    // Pie chart
    pieChartData.value = {
      labels: ['Occupied', 'Non-Occupied'],
      datasets: [
        {
          label: 'Total Slots',
          backgroundColor: ['#f87171', '#60a5fa'],
          data: [data.pie_chart.occupied, data.pie_chart.non_occupied]
        }
      ]
    }
  } catch (error) {
    console.error('Error fetching chart data:', error)
  }
})
</script>
<style>
.container {
  max-width: 800px;
}
</style>
