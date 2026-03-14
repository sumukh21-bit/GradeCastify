<script setup>
import { inject, ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import Navbar from '../components/Navbar.vue'

const supabase = inject('supabase')
const displayName = ref('User')

onMounted(async () => {
  const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

  if (isDemoAdmin) {
    displayName.value = 'Demo Admin'
    return
  }

  const { data: { session } } = await supabase.auth.getSession()

  if (session?.user?.email) {
    displayName.value = session.user.email
  } else {
    displayName.value = 'User'
  }
})
</script>

<template>
  <div class="gc-dashboard-shell is-flex">
    <Sidebar class="gc-sidebar" />

    <div class="gc-main-column">
      <Navbar />

      <section class="section gc-main-panel">
        <div class="mb-5">
          <h1 class="title has-text-white mb-2">Dashboard</h1>
          <p class="subtitle is-6 has-text-grey-light">Welcome back, {{ displayName }}</p>
        </div>

        <div class="columns is-variable is-4 mb-2">
          <div class="column">
            <div class="box gc-soft-box">
              <p class="has-text-grey-light mb-2">Current GPA</p>
              <p class="title has-text-white mb-0">3.72</p>
            </div>
          </div>

          <div class="column">
            <div class="box gc-soft-box">
              <p class="has-text-grey-light mb-2">Courses Tracked</p>
              <p class="title has-text-white mb-0">6</p>
            </div>
          </div>

          <div class="column">
            <div class="box gc-soft-box">
              <p class="has-text-grey-light mb-2">Predicted Final</p>
              <p class="title has-text-white mb-0">A-</p>
            </div>
          </div>
        </div>

        <div class="box gc-soft-box mb-4">
          <div class="is-flex is-justify-content-space-between is-align-items-center mb-4">
            <div>
              <h2 class="title is-4 has-text-white mb-1">Course Overview</h2>
              <p class="is-size-7 has-text-grey-light mb-0">Track your current standing and targets</p>
            </div>

            <div class="buttons are-small mb-0">
              <button class="button is-dark is-outlined">Filter</button>
              <button class="button gc-accent-btn">Add Course</button>
            </div>
          </div>

          <div class="table-container">
            <table class="table is-fullwidth is-hoverable gc-table">
              <thead>
                <tr>
                  <th class="has-text-white">Course</th>
                  <th class="has-text-white">Current</th>
                  <th class="has-text-white">Target</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Algorithms</td>
                  <td>81%</td>
                  <td>85%</td>
                </tr>
                <tr>
                  <td>Database Systems</td>
                  <td>76%</td>
                  <td>80%</td>
                </tr>
                <tr>
                  <td>Web Development</td>
                  <td>88%</td>
                  <td>90%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="columns is-variable is-4">
          <div class="column">
            <div class="box gc-soft-box">
              <h2 class="title is-5 has-text-white">Performance Trend</h2>
              <p class="has-text-grey-light">
                Recent academic performance metrics will appear here.
              </p>
            </div>
          </div>

          <div class="column">
            <div class="box gc-soft-box">
              <h2 class="title is-5 has-text-white">Recommendations</h2>
              <p class="has-text-grey-light">
                Smart suggestions and GPA guidance will appear here.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>