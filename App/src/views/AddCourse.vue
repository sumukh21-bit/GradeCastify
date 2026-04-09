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

const optionalNum = (v) => v === '' ? null : Number(v)

// submit course
const submit = async () => {
  error.value = ''
  loading.value = true

  try {
    const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

    // demo mode -> save directly to csv
    if (isDemoAdmin) {
      const scoreForGrade = optionalNum(midtermScore.value) ?? 0

      const saveResponse = await fetch('http://localhost:3001/api/courses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          course: courseName.value,
          current: scoreForGrade,
          attendance: optionalNum(attendance.value),
          midterm_score: optionalNum(midtermScore.value),
          assignments_avg: optionalNum(assignmentsAvg.value),
          quizzes_avg: optionalNum(quizzesAvg.value),
          participation_score: optionalNum(participationScore.value),
          projects_score: optionalNum(projectsScore.value),
          predicted_grade:
            scoreForGrade >= 85 ? 'A'
            : scoreForGrade >= 75 ? 'B'
            : scoreForGrade >= 65 ? 'C'
            : scoreForGrade >= 50 ? 'D'
            : 'F'
        }),
      })

      if (!saveResponse.ok) {
        throw new Error('failed to save course to csv')
      }

      router.push('/')
      return
    }

    // normal login mode
    const { data: { session } } = await supabase.auth.getSession()
    const userId = session?.user?.id

    if (!userId) {
      throw new Error('you are not logged in')
    }

    const { data: profile } = await supabase
      .from('student_profile')
      .select('*')
      .eq('user_id', userId)
      .single()

    if (!profile) {
      throw new Error('please fill out your profile information before adding a course.')
    }

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

    if (!response.ok) {
      throw new Error('prediction request failed')
    }

    const { grade } = await response.json()

    const saveResponse = await fetch('http://localhost:3001/api/courses', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        course: courseName.value,
        current: optionalNum(midtermScore.value) ?? 0,
        attendance: optionalNum(attendance.value),
        midterm_score: optionalNum(midtermScore.value),
        assignments_avg: optionalNum(assignmentsAvg.value),
        quizzes_avg: optionalNum(quizzesAvg.value),
        participation_score: optionalNum(participationScore.value),
        projects_score: optionalNum(projectsScore.value),
        predicted_grade: grade
      }),
    })

    if (!saveResponse.ok) {
      throw new Error('failed to save course to csv')
    }

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
      <button type="button" @click="router.push('/')">Back</button>
    </form>
  </div>
</template>
