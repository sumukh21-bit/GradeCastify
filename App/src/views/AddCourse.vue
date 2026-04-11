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

    <div class="main-area">
      <div class="main-wrap profile-wrap">
        <button type="button" class="back-link" @click="router.push('/')"> ← Back </button>

        <section class="page-head">
          <h1 class="title has-text-white mb-2">Add Course</h1>
          <p class="has-text-grey-light">
            Enter your course details to get a predicted grade.
          </p>
        </section>

        <form class="profile-form" @submit.prevent="submit">
          <div class="box info-card section-card">
            <div class="section-head">
              <h2 class="section-title">Course Information</h2>
              <p class="section-subtitle">Enter the details for your new course.</p>
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
              <p class="section-subtitle">Enter your grade for each category.</p>
            </div>

            <div class="stack-fields">
              <div class="field">
                 <div>
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
              </div>

              <div class="field">
                <div>
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
              </div>

              <div class="field">
                <div>
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
              </div>

              <div class="field">
                <div>
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
              </div>

              <div class="field">
                <div>
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
            </div>
            <div class="form-footer">
              <div class="form-message">
                <p v-if="error">{{ error }}</p>
              </div>

              <button class="button is-primary save-btn" type="submit" :disabled="loading">
                {{ loading ? 'Saving...' : 'Submit & Predict Grade' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
