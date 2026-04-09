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

// profile fields
const studyHours = ref('')
const hasExtracurriculars = ref(false)
const stressLevel = ref('')
const sleepHours = ref('')

// load existing profile on mount
onMounted(async () => {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.user?.id) return
  const { data: profile } = await supabase
    .from('student_profile')
    .select('*')
    .eq('user_id', session.user.id)
    .single()
  if (profile) {
    studyHours.value = profile.study_hours_per_week ?? ''
    hasExtracurriculars.value = profile.has_extracurriculars ?? false
    stressLevel.value = profile.stress_level ?? ''
    sleepHours.value = profile.sleep_hours_per_night ?? ''
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

    const { error: err } = await supabase
      .from('student_profile')
      .upsert({
        user_id: userId,
        study_hours_per_week: Number(studyHours.value),
        has_extracurriculars: hasExtracurriculars.value,
        stress_level: Number(stressLevel.value),
        sleep_hours_per_night: Number(sleepHours.value),
      })
    if (err) throw err
    saved.value = true
  } catch (err) {
    error.value = err.message || 'something went wrong'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <!-- Repreaded code -->
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
    <!-- Repreaded code -->

    <div class="main-area">
      <div class="main-warp">
        <button type="button" @click="router.push('/')">Back</button>
        <section class="page-head">
          <h1 class="title has-text-white mb-2">My Profile</h1>
          <p class="has-text-grey-light">Metrics used across all your grade predictions.</p>
        </section>
        
        <form @submit.prevent="save">
          <div class="columns is-variable is-3 top-cards">
            <div class="column">
              <div class="box info-card">
                <div class="field">
                  <label class="label">Study Hours / Week</label>
                  <input class="input" type="number" min="0" v-model="studyHours" required />
                </div>
              </div>
            </div>

            <div class="column">
              <div class="box info-card">
                <div class="field">
                  <label class="label">Sleep Hours / Night</label>
                  <input class="input" type="number" min="0" max="24" step="0.5" v-model="sleepHours" required />
                </div>
              </div>
            </div>
          </div>

          <div class="columns is-variable is-3 top-cards">
            <div class="column">
              <div class="box info-card">
                <div class="field">
                  <label class="label">Stress Level (1-10)</label>
                  <input class="input" type="number" min="1" max="10" v-model="stressLevel" required />
                </div>
              </div>
            </div>

            <div class="column">
              <div class="box info-card">
                <div class="field">
                  <label class="label">Extracurriculars</label>
                  <input class="input" type="checkbox" v-model="hasExtracurriculars" />
                </div>
              </div>
            </div>
          </div>

          <p v-if="error">{{ error }}</p>
          <p v-if="saved">Saved!</p>

          <div class="buttons is-centered">
            <button class="button is-primary" type="submit" :disabled="loading">
              {{ loading ? 'Saving...' : 'Save Profile' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
