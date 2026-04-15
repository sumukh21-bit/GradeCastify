<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const supabase = inject('supabase')

const noteText = ref('')
const saved = ref(false)
const displayName = ref('')
const upcomingDue = ref('Lab 4 due Mar 20')

// sidebar state
const sidebarOpen = ref(false)

onMounted(async () => {
  if (!supabase) return
  try {
    const { data } = await supabase.auth.getSession()
    const session = data.session
    if (!session) return

    if (session?.user?.email) {
      displayName.value = session.user.email
    }

    const { data: noteData } = await supabase
      .from('notes')
      .select('content')
      .eq('user_id', session.user.id)
      .single()
    if (noteData) noteText.value = noteData.content
  } catch (err) {
    console.log('session error:', err)
  }
})

const saveNote = async () => {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) return
  await supabase.from('notes').upsert({ user_id: session.user.id, content: noteText.value, updated_at: new Date().toISOString() })
  saved.value = true
  setTimeout(() => { saved.value = false }, 1500)
}

const clearNote = async () => {
  noteText.value = ''
  saved.value = false
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) return
  await supabase.from('notes').upsert({ user_id: session.user.id, content: '', updated_at: new Date().toISOString() })
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

const goToAddCourse = () => {
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
              <li><a @click="() => { closeSidebar(); router.push('/') }">Dashboard</a></li>
              <li><a @click="goToAddCourse">Add Course</a></li>
              <li><a @click="() => { closeSidebar(); router.push('/profile') }">My Profile</a></li>
              <li><a class="is-active">Note Editor</a></li>
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
            <h1 class="title has-text-white mb-2">Note Editor</h1>
            <p class="has-text-grey-light">
              Paste and keep text. Your note is saved to your account.
            </p>
          </section>

          <div class="box info-card section-card">
            <div class="field">
              <label class="label">Note</label>
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
                <p v-if="saved" class="saved-text">Saved</p>
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
  </div>
</template>
