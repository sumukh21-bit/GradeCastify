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
  <div>
    <button type="button" @click="router.push('/')">Back</button>
    <h1>My Profile</h1>
    <p>Metrics used across all your grade predictions.</p>

    <form @submit.prevent="save">
      <div>
        <label>Study Hours / Week</label>
        <input type="number" min="0" v-model="studyHours" required />
      </div>

      <div>
        <label>Sleep Hours / Night</label>
        <input type="number" min="0" max="24" step="0.5" v-model="sleepHours" required />
      </div>

      <div>
        <label>Stress Level (1-10)</label>
        <input type="number" min="1" max="10" v-model="stressLevel" required />
      </div>

      <div>
        <label>Extracurriculars</label>
        <input type="checkbox" v-model="hasExtracurriculars" />
      </div>

      <p v-if="error">{{ error }}</p>
      <p v-if="saved">Saved!</p>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Saving...' : 'Save Profile' }}
      </button>
    </form>
  </div>
</template>
