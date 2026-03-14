<script setup>
import 'bulma/css/bulma.css'
import { inject, ref, onMounted } from 'vue'
import logo from '../logo.png'

const supabase = inject('supabase')
const displayName = ref('User')
const currentView = ref('dashboard')

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

const handleSignOut = async () => {
  localStorage.removeItem('gc_demo_admin')

  if (supabase) {
    await supabase.auth.signOut()
  }

  window.location.reload()
}

onMounted(async () => {
  const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

  if (isDemoAdmin) {
    displayName.value = 'Demo Admin'
    return
  }

  if (!supabase) {
    displayName.value = 'User'
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
    <aside class="menu p-4 gc-sidebar is-flex is-flex-direction-column is-justify-content-space-between">
      <div>
        <div class="is-flex is-align-items-center mb-5">
          <img :src="logo" alt="GradeCastify logo" style="width: 42px; height: 42px;" />
          <div class="ml-3">
            <p class="has-text-weight-bold is-size-5 has-text-white mb-1">GradeCastify</p>
            <p class="is-size-7 has-text-grey-light">Student Dashboard</p>
          </div>
        </div>

        <p class="menu-label has-text-grey-light">Workspace</p>
        <ul class="menu-list">
          <li>
            <a
              class="has-text-white"
              :class="{ 'is-active': currentView === 'dashboard' }"
              @click="currentView = 'dashboard'"
            >
              Dashboard
            </a>
          </li>

          <li>
            <a
              class="has-text-white"
              :class="{ 'is-active': currentView === 'add-course' }"
              @click="currentView = 'add-course'"
            >
              Add Course
            </a>
          </li>

          <li>
            <a href="/group_members.html" class="has-text-white">
              Group Member
            </a>
          </li>
        </ul>
      </div>

      <div>
        <div class="box gc-soft-box mb-3">
          <p class="has-text-weight-semibold has-text-white">{{ displayName }}</p>
          <p class="is-size-7 has-text-grey-light">
            {{ displayName === 'Demo Admin' ? 'Testing Account' : 'Signed-in User' }}
          </p>
        </div>

        <button class="button is-fullwidth gc-accent-btn has-text-weight-semibold" @click="handleSignOut">
          Sign out
        </button>
      </div>
    </aside>

    <div class="gc-main-column">
      <nav class="navbar gc-topbar px-5 py-3" role="navigation" aria-label="dashboard topbar">
        <div class="navbar-brand">
          <div class="navbar-item pl-0">
            <div>
              <p class="gc-topbar-label mb-1">Workspace</p>
              <h2 class="gc-topbar-title">
                {{ currentView === 'dashboard' ? 'Dashboard' : 'Add Course' }}
              </h2>
            </div>
          </div>
        </div>

        <div class="navbar-menu is-active">
          <div class="navbar-end">
            <div class="navbar-item">
              <span class="gc-topbar-status">
                {{ currentView === 'dashboard' ? 'Student dashboard' : 'Course creation' }}
              </span>
            </div>
          </div>
        </div>
      </nav>

      <section class="section gc-main-panel">
        <template v-if="currentView === 'dashboard'">
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
                <button class="button gc-accent-btn" @click="currentView = 'add-course'">
                  Add Course
                </button>
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
        </template>

        <template v-else-if="currentView === 'add-course'">
          <div class="mb-5">
            <h1 class="title has-text-white mb-2">Add Course</h1>
            <p class="subtitle is-6 has-text-grey-light">
              Create a course and define its target and components.
            </p>
          </div>

          <div class="columns">
            <div class="column is-8">
              <div class="box gc-soft-box p-5">
                <div class="field">
                  <label class="label has-text-light">Course Name</label>
                  <div class="control">
                    <input
                      class="input gc-login-input"
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
                      class="input gc-login-input"
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

                <div class="buttons mt-4">
                  <button class="button is-light" @click="addComponent">
                    + Add Component
                  </button>
                  <button class="button gc-accent-btn">
                    Save Course
                  </button>
                  <button class="button gc-ghost-btn" @click="currentView = 'dashboard'">
                    Back to Dashboard
                  </button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </section>
    </div>
  </div>
</template>
