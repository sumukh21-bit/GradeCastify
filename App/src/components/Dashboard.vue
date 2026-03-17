<script setup>
import { inject, ref, onMounted } from 'vue'
<<<<<<< HEAD


const supabase = inject('supabase')
const displayName = ref('User')

onMounted(async () => {
=======
import { useRouter } from 'vue-router'

const router = useRouter()
const supabase = inject('supabase')

const displayName = ref('User')
const sidebarOpen = ref(false)
const upcomingDue = ref('Lab 4 due Mar 20')

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

onMounted(async () => {
  if (debug) {
    console.log('dashboard mounted')
  }

>>>>>>> Zeyu_Branch
  const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

  if (isDemoAdmin) {
    displayName.value = 'Demo Admin'
<<<<<<< HEAD
    return
  }

  const { data: { session } } = await supabase.auth.getSession()

  if (session?.user?.email) {
    displayName.value = session.user.email
  } else {
    displayName.value = 'User'
=======

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
  } catch (err) {
    console.log('session error:', err)
>>>>>>> Zeyu_Branch
  }
})
</script>

<<<<<<< HEAD
<template >
     <nav>
      
      <div class="navbar-end">
        <nav class="navbar-start title">Grade<h1 class="has-text-success title">Castify</h1></nav>
      <a class="is-size-6 navbar-item">
        Sign out
      </a>
      <a class="is-size-6 navbar-item is-rounded" href="group_members.html">
        <button class="has-background-white">{{ displayName }}</button>
      </a>
      
    </div>

     </nav>
  <div>
 
       <h1 class="title is-size-2 has-text-success has-text-centered mt-6">Dashboard</h1>
    

  </div>
 
  <div class="mainContainer  mt-4 columns is-centered">
    
    <div class="  column is-2">
      <div class="box">
        <h1 class="is-size-8">Current Average</h1>
       <h2 class="is-size-3">0</h2></div>
       
    </div>
    <div class="  column is-2">
      <div class="box">
        <h1 class="is-size-8">Predicted Average</h1>
       <h2 class="is-size-3">0</h2></div>
       
    </div>
    <div class="  column is-2">
      <div class="box"> 
        <h1 class="is-size-8">Courses Taken</h1>
       <h2 class="is-size-3">0</h2></div>
      
    </div>
  </div>

  <div class="Courses px-6 column is-8">
    <h1 class="title px-6 has-text-centered">My Courses <button class="navbar-end mb-6">+ Add</button></h1>
    

  </div>
</template> 
=======
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
              <li><a>Settings</a></li>
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
                <p class="title is-3 has-text-white mb-0">0</p>
              </div>
            </div>

            <div class="column">
              <div class="box info-card">
                <p class="heading has-text-grey-light">Predicted Average</p>
                <p class="title is-3 has-text-white mb-0">0</p>
              </div>
            </div>

            <div class="column">
              <div class="box info-card">
                <p class="heading has-text-grey-light">Courses Taken</p>
                <p class="title is-3 has-text-white mb-0">0</p>
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

                <div class="box empty-card">
                  <p class="has-text-white has-text-weight-semibold mb-1">No courses added yet.</p>
                  <p class="has-text-grey is-size-7">Add a course to get started.</p>
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
>>>>>>> Zeyu_Branch
