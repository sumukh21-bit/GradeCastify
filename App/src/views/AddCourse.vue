<script setup>
import { inject, ref } from 'vue'
import { useRouter } from 'vue-router'

// set up supabase client and router
const supabase = inject('supabase')
const router = useRouter()

// component state
const loading = ref(false)
const error = ref('')

// course fields
const courseName = ref('')
const attendance = ref('')
const midtermScore = ref('')
const assignmentsAvg = ref('')
const quizzesAvg = ref('')
const participationScore = ref('')
const projectsScore = ref('')

// submit course and get grade prediction
const submit = async () => {
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

    // save course with predicted grade to database
    const { error: courseErr } = await supabase
      .from('courses')
      .insert({
        user_id: userId,
        course_name: courseName.value,
        attendance: optionalNum(attendance.value),
        midterm_score: optionalNum(midtermScore.value),
        assignments_avg: optionalNum(assignmentsAvg.value),
        quizzes_avg: optionalNum(quizzesAvg.value),
        participation_score: optionalNum(participationScore.value),
        projects_score: optionalNum(projectsScore.value),
        predicted_grade: grade,
      })
    if (courseErr) throw courseErr

    // navigate back to dashboard after saving
    router.push('/')
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
    <h1>Add Course</h1>

    <form @submit.prevent="submit">
      <div>
        <label>Course Name</label>
        <input v-model="courseName" required />
      </div>

      <div>
        <label>Attendance (%)</label>
        <input type="number" min="0" max="100" v-model="attendance" />
      </div>

      <div>
        <label>Midterm Score</label>
        <input type="number" min="0" max="100" v-model="midtermScore" />
      </div>

      <div>
        <label>Assignments Avg</label>
        <input type="number" min="0" max="100" v-model="assignmentsAvg" />
      </div>

      <div>
        <label>Quizzes Avg</label>
        <input type="number" min="0" max="100" v-model="quizzesAvg" />
      </div>

      <div>
        <label>Participation Score</label>
        <input type="number" min="0" max="100" v-model="participationScore" />
      </div>

      <div>
        <label>Projects Score</label>
        <input type="number" min="0" max="100" v-model="projectsScore" />
      </div>

      <p v-if="error">{{ error }}</p>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Saving...' : 'Submit & Predict Grade' }}
      </button>
    </form>
  </div>
</template>
