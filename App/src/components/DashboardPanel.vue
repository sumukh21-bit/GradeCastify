<script setup>
defineProps({
  displayName: {
    type: String,
    default: 'Demo Admin'
  }
})

defineEmits(['sign-out'])
</script>

<template>
  <div class="p-4">
    <div class="has-text-centered mb-5">
      <h2 class="title is-3 has-text-white">Dashboard</h2>
      <p class="has-text-grey-light">
        Welcome, <strong>{{ displayName }}</strong>
      </p>
    </div>

    <div class="columns is-multiline">
      <div class="column is-4">
        <div class="box has-background-dark">
          <p class="heading has-text-grey-light">Current GPA</p>
          <p class="title is-4 has-text-white">3.72</p>
        </div>
      </div>

      <div class="column is-4">
        <div class="box has-background-dark">
          <p class="heading has-text-grey-light">Courses Tracked</p>
          <p class="title is-4 has-text-white">6</p>
        </div>
      </div>

      <div class="column is-4">
        <div class="box has-background-dark">
          <p class="heading has-text-grey-light">Predicted Final</p>
          <p class="title is-4 has-text-white">A-</p>
        </div>
      </div>

      <div class="column is-12">
        <div class="box has-background-dark">
          <p class="title is-5 has-text-white mb-4">Course Overview</p>
          <table class="table is-fullwidth is-striped">
            <thead>
              <tr>
                <th>Course</th>
                <th>Current</th>
                <th>Target</th>
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
    </div>

    <div class="has-text-centered mt-4">
      <button class="button is-primary" @click="$emit('sign-out')">
        Sign out
      </button>
    </div>
  </div>
</template>
