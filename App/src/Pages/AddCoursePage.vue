<script setup>
import 'bulma/css/bulma.css'
import { ref } from 'vue'

const courseName = ref('')
const targetGrade = ref('')

const components = ref([
  { name: 'Midterm 1', weight: '20' }
])

const addComponent = () => {
  components.value.push({
    name: '',
    weight: ''
  })
}
</script>

<template>
  <section class="section">
    <div class="container">
      <div class="columns is-centered">
        <div class="column is-6">
          <div class="box has-background-grey-darker p-5">
            <h1 class="title has-text-white has-text-centered">Add Course</h1>

            <div class="field">
              <label class="label has-text-light">Course Name</label>
              <div class="control">
                <input
                  class="input"
                  type="text"
                  v-model="courseName"
                  placeholder="Enter course name"
                />
              </div>
            </div>

            <div class="field">
              <label class="label has-text-light">Target Grade</label>
              <div class="control">
                <input
                  class="input"
                  type="number"
                  v-model="targetGrade"
                  placeholder="Enter target grade"
                />
              </div>
            </div>

            <div class="mt-5 mb-3">
              <h2 class="title is-5 has-text-white">Course Components</h2>
            </div>

            <div
              class="box has-background-dark mb-4"
              v-for="(component, index) in components"
              :key="index"
            >
              <div class="field">
                <label class="label has-text-light">
                  Component Name {{ index + 1 }}
                </label>
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    v-model="component.name"
                    placeholder="Example: Midterm 1"
                  />
                </div>
              </div>

              <div class="field">
                <label class="label has-text-light">Weight (%)</label>
                <div class="control">
                  <input
                    class="input"
                    type="number"
                    v-model="component.weight"
                    placeholder="Example: 20"
                  />
                </div>
              </div>
            </div>

            <div class="buttons is-centered mt-4">
              <button class="button is-light" @click="addComponent">
                + Add Component
              </button>
              <button class="button is-primary">
                Save Course
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
