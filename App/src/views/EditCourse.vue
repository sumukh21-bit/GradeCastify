<script setup>
import { inject, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// set up supabase client, router, and route
const supabase = inject('supabase')
const router = useRouter()
const route = useRoute()
const id = route.params.id

// component state
const loading = ref(false)
const error = ref('')
const displayName = ref('')
const upcomingDue = ref('Lab 4 due Mar 20')

// sidebar state
const sidebarOpen = ref(false)

// course fields
const courseName = ref('')
const attendance = ref('')
const midtermScore = ref('')
const assignmentsAvg = ref('')
const quizzesAvg = ref('')
const participationScore = ref('')
const projectsScore = ref('')

// load existing course data on mount
onMounted(async () => {
  if (!supabase) return
  try {
    const { data } = await supabase.auth.getSession()
    const session = data.session
    if (!session?.user?.id) return

    if (session?.user?.email) {
      displayName.value = session.user.email
    }

    const { data: course } = await supabase
      .from('courses')
      .select('*')
      .eq('id', id)
      .single()
    if (course) {
      courseName.value = course.course_name ?? ''
      attendance.value = course.attendance ?? ''
      midtermScore.value = course.midterm_score ?? ''
      assignmentsAvg.value = course.assignments_avg ?? ''
      quizzesAvg.value = course.quizzes_avg ?? ''
      participationScore.value = course.participation_score ?? ''
      projectsScore.value = course.projects_score ?? ''
    }
  } catch (err) {
    console.log('session error:', err)
  }
})

// submit course updates and get new grade prediction
const save = async () => {
  // reset error and set loading state
  error.value = ''
  loading.value = true
  // get user profile for prediction
  try {
    const { data: { session } } = await supabase.auth.getSession()
    const userId = session?.user?.id
    if (!userId) throw new Error('you are not logged in')

    const { data: profile } = await supabase
      .from('student_profile')
      .select('*')
      .eq('user_id', userId)
      .single()

    if (!profile) {
      throw new Error('please fill out your profile information before adding a course.')
    }

    // convert empty strings to null and valid numbers to Number type
    const optionalNum = (v) => v === '' ? null : Number(v)

    // send data to prediction endpoint
    const response = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        attendance: optionalNum(attendance.value),
        midterm_score: optionalNum(midtermScore.value),
        assignments_avg: optionalNum(assignmentsAvg.value),
        quizzes_avg: optionalNum(quizzesAvg.value),
        participation_score: optionalNum(participationScore.value),
        projects_score: optionalNum(projectsScore.value),
        study_hours_per_week: profile.study_hours_per_week,
        has_extracurriculars: profile.has_extracurriculars,
        stress_level: profile.stress_level,
        sleep_hours_per_night: profile.sleep_hours_per_night,
      }),
    })
    if (!response.ok) throw new Error('prediction request failed')
    const { grade } = await response.json()

    // update course with new data and predicted grade
    const { error: err } = await supabase
      .from('courses')
      .update({
        course_name: courseName.value,
        attendance: optionalNum(attendance.value),
        midterm_score: optionalNum(midtermScore.value),
        assignments_avg: optionalNum(assignmentsAvg.value),
        quizzes_avg: optionalNum(quizzesAvg.value),
        participation_score: optionalNum(participationScore.value),
        projects_score: optionalNum(projectsScore.value),
        predicted_grade: grade,
      })
      .eq('id', id)
    if (err) throw err
    // navigate back to dashboard after saving
    router.push('/')
  } catch (err) {
    error.value = err.message || 'something went wrong'
  } finally {
    loading.value = false
  }
}

// sidebar toggle functions with debug logging
const debug = true

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value

  if (debug) {
    console.log('sidebar toggled:', sidebarOpen.value)
  }

}

const closeSidebar = () => {
  sidebarOpen.value = false

  if (debug) {
    console.log('sidebar closed')
  }

}

const goToAddCourse = () => {
  closeSidebar()
  router.push('/add-course')
}

const handleSignOut = async () => {
  closeSidebar()

  if (debug) {
    console.log('sign out started')
  }

  localStorage.removeItem('gc_demo_admin')

  try {
    if (supabase) {
      await supabase.auth.signOut()

      if (debug) {
        console.log('supabase signed out')
      }
    }
  } catch (err) {
    console.log('sign out error:', err)
  }

  router.push('/')
}
</script>

<template>
  <div class="dashboard-page">
    <header class="top-bar">
      <div class="top-bar-inner">
        <div class="top-left">
          <button type="button" class="button menu-btn" @click="toggleSidebar">☰</button>

          <div class="logo-text">
            <span class="logo-main">Grade</span>
            <span class="logo-accent">Castify</span>
          </div>
        </div>
      </div>
    </header>

    <div class="main-layer">
      <div class="overlay-bg" :class="{ active: sidebarOpen }" @click="closeSidebar"></div>

      <aside class="side-menu" :class="{ open: sidebarOpen }">
        <div class="side-inner">
          <div class="box user-card mb-4">
            <p class="is-size-7 has-text-grey mb-2">User</p>
            <p class="has-text-white has-text-weight-semibold user-email">{{ displayName }}</p>
          </div>

          <aside class="menu mb-5">
            <p class="menu-label">Menu</p>
            <ul class="menu-list">
              <li><a @click="() => { closeSidebar(); router.push('/') }">Dashboard</a></li>
              <li><a @click="goToAddCourse">Add Course</a></li>
              <li><a @click="() => { closeSidebar(); router.push('/profile') }">My Profile</a></li>
              <li><a @click="() => { closeSidebar(); router.push('/note-editor') }">Note Editor</a></li>
            </ul>
          </aside>

          <div class="box due-card mb-5">
            <p class="is-size-7 has-text-grey mb-2">Next deadline</p>
            <p class="has-text-white">{{ upcomingDue }}</p>
          </div>

          <button type="button" class="button logout-btn is-fullwidth" @click="handleSignOut">
            Sign out
          </button>
        </div>
      </aside>

      <div class="main-area">
        <div class="main-wrap profile-wrap">
          <section class="page-head">
            <h1 class="title has-text-white mb-2">Edit Course</h1>
            <p class="has-text-grey-light">
              Update your course details to get a new predicted grade.
            </p>
          </section>

          <form class="profile-form" @submit.prevent="save">
            <div class="box info-card section-card">
              <div class="section-head">
                <h2 class="section-title">Course Information</h2>
                <p class="section-subtitle">Update the details for this course.</p>
              </div>

              <div class="stack-fields">
                <div class="field">
                  <label class="label">Course Name</label>
                  <div class="control">
                    <input
                      class="input"
                      type="text"
                      v-model="courseName"
                      placeholder="e.g. Introduction to Computer Science"
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Attendance (%)</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      max="100"
                      v-model="attendance"
                      placeholder="e.g. 95"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="box info-card section-card">
              <div class="section-head">
                <h2 class="section-title">Grade Information</h2>
                <p class="section-subtitle">Update your grade for each category.</p>
              </div>

              <div class="stack-fields">
                <div class="field">
                  <label class="label">Midterm Score</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      max="100"
                      v-model="midtermScore"
                      placeholder="e.g. 75"
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Assignments Avg</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      max="100"
                      v-model="assignmentsAvg"
                      placeholder="e.g. 80"
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Quizzes Avg</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      max="100"
                      v-model="quizzesAvg"
                      placeholder="e.g. 85"
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Participation Score</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      max="100"
                      v-model="participationScore"
                      placeholder="e.g. 95"
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Projects Score</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      max="100"
                      v-model="projectsScore"
                      placeholder="e.g. 95"
                    />
                  </div>
                </div>
              </div>

              <div class="form-footer">
                <div class="form-message">
                  <p v-if="error" class="error-text">{{ error }}</p>
                </div>

                <button class="button is-primary save-btn" type="submit" :disabled="loading">
                  {{ loading ? 'Saving...' : 'Save & Predict Grade' }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
