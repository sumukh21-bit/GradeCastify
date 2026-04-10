<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const noteText = ref('')
const saved = ref(false)

const toggleSidebar = () => {}

onMounted(() => {
  const savedNote = sessionStorage.getItem('gc_note_editor')
  if (savedNote) {
    noteText.value = savedNote
  }
})

const saveNote = () => {
  sessionStorage.setItem('gc_note_editor', noteText.value)
  saved.value = true

  setTimeout(() => {
    saved.value = false
  }, 1500)
}

const clearNote = () => {
  noteText.value = ''
  sessionStorage.removeItem('gc_note_editor')
  saved.value = false
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
        <button type="button" class="back-link" @click="router.push('/')">
          ← Back
        </button>

        <section class="page-head">
          <h1 class="title has-text-white mb-2">Note_Editor</h1>
          <p class="has-text-grey-light">
            Paste and keep temporary text for this session. It clears when you sign out.
          </p>
        </section>

        <div class="box info-card section-card">
          <div class="field">
            <label class="label">Session Note</label>
            <div class="control">
              <textarea
                v-model="noteText"
                class="textarea note-editor-area"
                rows="18"
                placeholder="Paste or type your text here..."
              ></textarea>
            </div>
          </div>

          <div class="form-footer">
            <div class="form-message">
              <p v-if="saved" class="saved-text">Saved for this session</p>
            </div>

            <div class="note-buttons">
              <button class="button is-dark" type="button" @click="clearNote">
                Clear
              </button>
              <button class="button is-primary save-btn" type="button" @click="saveNote">
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
