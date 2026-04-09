<script setup>
import { inject, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const supabase = inject('supabase')

const displayName = ref('User')
const sidebarOpen = ref(false)
const upcomingDue = ref('Lab 4 due Mar 20')
const courses = ref([])
const loadingCourses = ref(false)
const coursesError = ref('')

const debug = true
const log = (...msg) => console.log('[Dashboard]', ...msg)

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

const loadDemoCoursesFromBackend = async () => {
  loadingCourses.value = true
  coursesError.value = ''

  try {
    log('start fetching demo courses')

    const res = await fetch('http://localhost:3001/api/courses')
    log('response status:', res.status)

    const data = await res.json()
    log('courses data:', data)

    courses.value = (data || []).map((item, index) => ({
      id: `demo-${index}`,
      course_name: item.course,
      predicted_grade:
        item.predicted_grade ||
        (
          item.current >= 85 ? 'A'
          : item.current >= 75 ? 'B'
          : item.current >= 65 ? 'C'
          : item.current >= 50 ? 'D'
          : 'F'
        ),
      attendance: item.attendance,
      midterm_score: item.midterm_score,
      assignments_avg: item.assignments_avg,
      quizzes_avg: item.quizzes_avg,
      participation_score: item.participation_score,
      projects_score: item.projects_score,
      is_demo: true
    }))

    if (debug) {
      console.log('demo backend courses loaded:', courses.value)
    }
  } catch (err) {
    console.log('demo backend load error:', err)
    console.error('[Dashboard] fetch failed:', err)
    coursesError.value = 'Could not load demo courses'
  } finally {
    loadingCourses.value = false
  }
}

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
  if (debug) console.log('sidebar toggled:', sidebarOpen.value)
}

const closeSidebar = () => {
  sidebarOpen.value = false
  if (debug) console.log('sidebar closed')
}

const deleteCourse = async (id) => {
  const targetCourse = courses.value.find(c => c.id === id)
  if (!targetCourse) return

  try {
    if (targetCourse.is_demo) {
      const res = await fetch(`http://localhost:3001/api/courses/${id}`, {
        method: 'DELETE'
      })

      if (!res.ok) {
        throw new Error('failed to delete demo course')
      }

      courses.value = courses.value.filter(c => c.id !== id)
      return
    }

    const { error } = await supabase.from('courses').delete().eq('id', id)
    if (error) throw error

    courses.value = courses.value.filter(c => c.id !== id)
  } catch (err) {
    console.log('delete course error:', err)
  }
}

const goToAddCourse = () => {
  if (debug) console.log('go to add course page')
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
      if (debug) console.log('supabase signed out')
    }
  } catch (err) {
    console.log('sign out error:', err)
  }

  window.location.reload()
}

onMounted(async () => {
  if (debug) {
    console.log('dashboard mounted')
  }

  const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'
  console.log('demo raw value:', localStorage.getItem('gc_demo_admin'))
  console.log('isDemoAdmin:', isDemoAdmin)
  log('mounted')
  log('isDemoAdmin:', isDemoAdmin)

  if (isDemoAdmin) {
    displayName.value = 'Demo Admin'
    if (debug) console.log('demo admin mode')
    await loadDemoCoursesFromBackend()
    return
  }

  if (!supabase) {
    if (debug) console.log('supabase not found')
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
      if (debug) console.log('user email loaded:', displayName.value)
    }

    if (session?.user?.id) {
      const { data: courseData } = await supabase
        .from('courses')
        .select('*')
        .eq('user_id', session.user.id)
        .order('created_at', { ascending: false })

      courses.value = courseData || []
    }
  } catch (err) {
    console.log('session error:', err)
  }
})
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
          </div>

          <div class="columns is-variable is-4 bottom-row">
            <div class="column is-7">
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

                <div v-if="loadingCourses" class="box empty-card">
                  <p class="has-text-white has-text-weight-semibold mb-1">Loading courses...</p>
                  <p class="has-text-grey is-size-7">Please wait a moment.</p>
                </div>

                <div v-else-if="coursesError" class="box empty-card">
                  <p class="has-text-white has-text-weight-semibold mb-1">{{ coursesError }}</p>
                  <p class="has-text-grey is-size-7">Check backend connection.</p>
                </div>

                <div v-else-if="courses.length === 0" class="box empty-card">
                  <p class="has-text-white has-text-weight-semibold mb-1">No courses added yet.</p>
                  <p class="has-text-grey is-size-7">Add a course to get started.</p>
                </div>

                <div
                  v-for="course in courses"
                  :key="course.id"
                  class="box empty-card mb-2"
                  style="display:flex; justify-content:space-between; align-items:center;"
                >
                  <div>
                    <p class="has-text-white has-text-weight-semibold mb-0">{{ course.course_name }}</p>
                    <p class="has-text-grey is-size-7">
                      Midterm: {{ course.midterm_score != null ? course.midterm_score : 'N/A' }}
                      |
                      Attendance: {{ course.attendance != null ? course.attendance : 'N/A' }}%
                      |
                      Assignments: {{ course.assignments_avg != null ? course.assignments_avg : 'N/A' }}%
                      |
                      Quizzes: {{ course.quizzes_avg != null ? course.quizzes_avg : 'N/A' }}%
                      |
                      Participation: {{ course.participation_score != null ? course.participation_score : 'N/A' }}%
                      |
                      Projects: {{ course.projects_score != null ? course.projects_score : 'N/A' }}%
                    </p>
                  </div>

                  <div style="display:flex; align-items:center; gap:0.75rem;">
                    <span class="tag is-medium" style="background:#27e1d1; color:#0b0f17; font-weight:700;">
                      {{ course.predicted_grade }}
                    </span>

                    <button
                      type="button"
                      class="button is-small is-danger is-light"
                      @click="deleteCourse(course.id)"
                    >
                      Delete
                    </button>

                    <button
                      v-if="!course.is_demo"
                      type="button"
                      class="button is-small"
                      @click="router.push(`/edit-course/${course.id}`)"
                    >
                      Edit
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="column is-5">
              <div class="box updates-panel">
                <h2 class="title is-5 has-text-white mb-4">Recent Activity</h2>

                <div class="update-item">
                  <p class="has-text-white mb-1">No updates yet.</p>
                  <p class="is-size-7 has-text-grey">-</p>
                </div>

                <div class="update-item">
                  <p class="has-text-white mb-1">Course changes show here.</p>
                  <p class="is-size-7 has-text-grey">-</p>
                </div>

                <div class="update-item">
                  <p class="has-text-white mb-1">Add a course to begin.</p>
                  <p class="is-size-7 has-text-grey">-</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>