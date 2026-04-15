<script setup>
import { inject, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

// set up supabase client and router
const supabase = inject('supabase')
const router = useRouter()

// component state
const loading = ref(false)
const saved = ref(false)
const error = ref('')

// basic profile fields
const email = ref('')
const displayName = ref('')
const program = ref('')
const yearOfStudy = ref('')

// prediction fields
const studyHours = ref('')
const hasExtracurriculars = ref(false)
const stressLevel = ref('')
const sleepHours = ref('')

// sidebar state
const sidebarOpen = ref(false)
const upcomingDue = ref('Lab 4 due Mar 20')

// load existing profile on mount
onMounted(async () => {
  try {
    const { data: { session } } = await supabase.auth.getSession()
    if (!session?.user?.id) return

    email.value = session.user.email || ''

    const { data: profile, error: profileError } = await supabase
      .from('student_profile')
      .select('*')
      .eq('user_id', session.user.id)
      .single()

    if (profileError && profileError.code !== 'PGRST116') {
      throw profileError
    }

    if (profile) {
      displayName.value = profile.display_name ?? ''
      program.value = profile.program ?? ''
      yearOfStudy.value = profile.year_of_study ?? ''
      studyHours.value = profile.study_hours_per_week ?? ''
      hasExtracurriculars.value = profile.has_extracurriculars ?? false
      stressLevel.value = profile.stress_level ?? ''
      sleepHours.value = profile.sleep_hours_per_night ?? ''
    }
  } catch (err) {
    error.value = err.message || 'failed to load profile'
  }
})

// save profile to database
const save = async () => {
  error.value = ''
  saved.value = false
  loading.value = true

  try {
    const { data: { session } } = await supabase.auth.getSession()
    const userId = session?.user?.id
    if (!userId) throw new Error('you are not logged in')

    const payload = {
      user_id: userId,
      display_name: displayName.value.trim(),
      program: program.value.trim(),
      year_of_study: yearOfStudy.value,
      study_hours_per_week: Number(studyHours.value),
      has_extracurriculars: hasExtracurriculars.value,
      stress_level: Number(stressLevel.value),
      sleep_hours_per_night: Number(sleepHours.value),
    }

    const { error: err } = await supabase
      .from('student_profile')
      .upsert(payload)

    if (err) throw err

    saved.value = true
    setTimeout(() => {
      saved.value = false
    }, 2000)
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
            <p class="has-text-white has-text-weight-semibold user-email">{{ email }}</p>
          </div>

          <aside class="menu mb-5">
            <p class="menu-label">Menu</p>
            <ul class="menu-list">
              <li><a @click="() => { closeSidebar(); router.push('/') }">Dashboard</a></li>
              <li><a @click="() => { closeSidebar(); router.push('/add-course') }">Add Course</a></li>
              <li><a class="is-active">My Profile</a></li>
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
            <h1 class="title has-text-white mb-2">My Profile</h1>
            <p class="has-text-grey-light">
              Manage your personal details and default prediction settings.
            </p>
          </section>

          <form class="profile-form" @submit.prevent="save">
            <div class="box info-card section-card">
              <div class="section-head">
                <h2 class="section-title">Basic Information</h2>
                <p class="section-subtitle">Your core account details.</p>
              </div>

              <div class="stack-fields">
                <div class="field">
                  <label class="label">Display Name</label>
                  <div class="control">
                    <input
                      class="input"
                      type="text"
                      v-model="displayName"
                      placeholder="Enter your name"
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Email</label>
                  <div class="control">
                    <input
                      class="input is-static profile-readonly"
                      type="email"
                      :value="email"
                      readonly
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Program</label>
                  <div class="control">
                    <input
                      class="input"
                      type="text"
                      v-model="program"
                      placeholder="e.g. Computer Science"
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Year of Study</label>
                  <div class="control">
                    <div class="select is-fullwidth">
                      <select v-model="yearOfStudy">
                        <option value="">Select year</option>
                        <option value="Year 1">Year 1</option>
                        <option value="Year 2">Year 2</option>
                        <option value="Year 3">Year 3</option>
                        <option value="Year 4">Year 4</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="box info-card section-card">
              <div class="section-head">
                <h2 class="section-title">Prediction Preferences</h2>
                <p class="section-subtitle">
                  These defaults are used across your grade predictions.
                </p>
              </div>

              <div class="stack-fields">
                <div class="field">
                  <label class="label">Study Hours / Week</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      v-model="studyHours"
                      required
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Sleep Hours / Night</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="0"
                      max="24"
                      step="0.5"
                      v-model="sleepHours"
                      required
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Stress Level (1–10)</label>
                  <div class="control">
                    <input
                      class="input"
                      type="number"
                      min="1"
                      max="10"
                      v-model="stressLevel"
                      required
                    />
                  </div>
                </div>

                <div class="field">
                  <label class="label">Extracurricular Activities</label>
                  <div class="control checkbox-row">
                    <label class="checkbox profile-checkbox">
                      <input type="checkbox" v-model="hasExtracurriculars" />
                      <span>I participate in extracurricular activities</span>
                    </label>
                  </div>
                </div>
              </div>

              <div class="form-footer">
                <div class="form-message">
                  <p v-if="error" class="error-text">{{ error }}</p>
                  <p v-else-if="saved" class="saved-text">Changes saved</p>
                </div>

                <button class="button is-primary save-btn" type="submit" :disabled="loading">
                  {{ loading ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>