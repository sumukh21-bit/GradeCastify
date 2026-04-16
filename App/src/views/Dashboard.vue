<script setup>
import { inject, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NoteEditor from './NoteEditor.vue'
import Profile from './Profile.vue'
import * as d3 from 'd3'
import $ from 'jquery'

const router = useRouter()
const supabase = inject('supabase')

const displayName = ref('User')
const sidebarOpen = ref(false)
const upcomingDue = ref('Lab 4 due Mar 20')
const courses = ref([])
const stressLevel = ref()

// helper to compute average score for a course, ignoring nulls
const getCourseAvg = (c) => {
  const scores = [
    c.midterm_score,
    c.assignments_avg,
    c.quizzes_avg,
    c.participation_score,
    c.projects_score
  ]

  let total = 0
  let count = 0

  for (let s of scores) {
    if (s != null) {
      total += Number(s)
      count++
    }
  }

  return count > 0 ? total / count : null
}

// compute average across all courses for display in top card
const currentAvg = computed(() => {
  const list = courses.value
  if (list.length === 0) return '-'

  let total = 0
  let count = 0

  for (let c of list) {
    const avg = getCourseAvg(c)
    if (avg != null) {
      total += avg
      count++
    }
  }

  if (count === 0) return '-'
  return (total / count).toFixed(1)
})

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

const deleteCourse = async (id) => {
  await supabase.from('courses').delete().eq('id', id)
  courses.value = courses.value.filter(c => c.id !== id)
}

const goToAddCourse = () => {

  if (debug) {
    console.log('go to add course page')
  }

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

// Function to draw a stress level bar using D3.js
const drawStressLevelBar = () => {
    let stressbar = d3.select('#stress-level-card')
      .append('svg')
      .attr('width', 300)
      .attr('height', 20)

    if (stressLevel.value > 0 && stressLevel.value <= 3) {
      stressbar.append('rect')
        .attr('width', (stressLevel.value / 10.0) * 300)
        .attr('height', 20)
        .attr('fill', 'green')
      $('#stress-response').text("Managing everything very well!, keep it up!");
    }

    if (stressLevel.value > 3 && stressLevel.value <= 7.0) {
      stressbar.append('rect')
        .attr('width', (stressLevel.value / 10.0) * 300)
        .attr('height', 20)
        .attr('fill', 'yellow')
      $('#stress-response').text("You're doing great! Consider taking short breaks to stay refreshed.");
    }

    if (stressLevel.value > 7.0 && stressLevel.value <= 10.0) {
      stressbar.append('rect')
        .attr('width', (stressLevel.value / 10.0) * 300)
        .attr('height', 20)
        .attr('fill', 'red')
      $('#stress-response').text("You're feeling overwhelmed. Take a break and prioritize your tasks.");
    }
    
    console.log('drawing stress level bar with value:', stressLevel.value)
  }

onMounted(async () => {
  if (debug) {
    console.log('dashboard mounted')
  }

  const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

  if (isDemoAdmin) {
    displayName.value = 'Demo Admin'

    if (debug) {
      console.log('demo admin mode')
    }

    return
  }

  if (!supabase) {
    if (debug) {
      console.log('supabase not found')
    }
    return
  }

  try {
    const { data } = await supabase.auth.getSession()
    const session = data.session

    if (debug) {
      console.log('session:', session)
    }

    if (session && session.user && session.user.email) {
      displayName.value = session.user.email

      if (debug) {
        console.log('user email loaded:', displayName.value)
      }
    }

    if (session?.user?.id) {
      const { data: courseData } = await supabase
        .from('courses')
        .select('*')
        .eq('user_id', session.user.id)
        .order('created_at', { ascending: false })
      courses.value = courseData || []

      const { data: profileData } = await supabase
        .from('student_profile')
        .select('stress_level')
        .eq('user_id', session.user.id)
        .single()
      stressLevel.value = profileData?.stress_level || ''
    }
  } catch (err) {
    console.log('session error:', err)
  }

  drawStressLevelBar()
})

const getPredictedGrade = (course) => {
  const avg = getCourseAvg(course)
  if (avg == null) return 'N/A'

  if (avg >= 90) return 'A'
  if (avg >= 80) return 'B'
  if (avg >= 70) return 'C'
  if (avg >= 60) return 'D'
  return 'F'
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
              <li><a class="is-active">Dashboard</a></li>
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

      <main class="main-area">
        <div class="main-wrap">
          <section class="page-head">
            <h1 class="title has-text-white mb-2">Dashboard</h1>
            <p class="has-text-grey-light">Overview of grades and updates.</p>
          </section>

          <div class="columns is-variable is-3 top-cards">
            <div class="column">
              <div class="box info-card">
                <p class="heading has-text-grey-light">Current Average</p>
                <p class="title is-3 has-text-white mb-0">{{ currentAvg }}</p>
              </div>
            </div>

            <div class="column">
              <div class="box info-card">
                <p class="heading has-text-grey-light">Courses Taken</p>
                <p class="title is-3 has-text-white mb-0">{{ courses.length }}</p>
              </div>
            </div>

            <div class="column">
              <div class="box info-card" id="stress-level-card">
                <p class="heading has-text-grey-light">Stress Level: {{ stressLevel }}</p>
                <p class="is-size-7 has-text-grey mt-1" id="stress-response"></p>
              </div> 
            </div>
              
          </div>

          

          <div class="columns is-variable is-4 bottom-row">
            <div class="column is-12">
              <div class="box course-panel">
                <div class="course-top mb-4">
                  <div>
                    <h2 class="title is-4 has-text-white mb-1">My Courses</h2>
                    <p class="has-text-grey-light is-size-7">Your courses will show here.</p>
                  </div>

                  <button type="button" class="button add-btn" @click="goToAddCourse">
                    + Add Course
                  </button>
                </div>

                <div v-if="courses.length === 0" class="box empty-card">
                  <p class="has-text-white has-text-weight-semibold mb-1">No courses added yet.</p>
                  <p class="has-text-grey is-size-7">Add a course to get started.</p>
                </div>

                <div
                  v-for="course in courses"
                  :key="course.id"
                  class="box empty-card mb-2 course-row"
                >
                  <div>
                    <p class="has-text-white has-text-weight-semibold mb-0">
                      {{ course.course_name }}
                    </p>
                    <p class="has-text-grey is-size-7">
                      Midterm: {{ course.midterm_score != null ? course.midterm_score : 'N/A' }} |
                      Attendance: {{ course.attendance != null ? course.attendance : 'N/A' }}% |
                      Assignments: {{ course.assignments_avg != null ? course.assignments_avg : 'N/A' }}% |
                      Quizzes: {{ course.quizzes_avg != null ? course.quizzes_avg : 'N/A' }}% |
                      Participation: {{ course.participation_score != null ? course.participation_score : 'N/A' }}% |
                      Projects: {{ course.projects_score != null ? course.projects_score : 'N/A' }}%
                    </p>
                  </div>

                  <div class="course-actions">
                    <span class="tag is-medium predicted-tag">
                      {{ getPredictedGrade(course) }}
                    </span>
                    <button type="button" class="delete" @click="deleteCourse(course.id)"></button>
                    <button type="button" @click="router.push(`/edit-course/${course.id}`)">Edit</button>
                  </div>
                </div>
              </div>
            </div>

  
          </div>
        </div>
      </main>
    </div>
  </div>
</template>