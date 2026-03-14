<script setup>
import 'bulma/css/bulma.css'
import DashboardPanel from './components/DashboardPanel.vue'
import { inject, ref, onMounted, onUnmounted } from 'vue'

const supabase = inject('supabase')
const email = ref('')
const password = ref('')
const user = ref(null)
const authListener = ref(null)
const isDemoAdmin = ref(false)

const signIn = async () => {
  await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value
  })
  email.value = ''
  password.value = ''
}

const signUp = async () => {
  await supabase.auth.signUp({
    email: email.value,
    password: password.value
  })
  email.value = ''
  password.value = ''
}

const enterDemoAdmin = () => {
  isDemoAdmin.value = true
}

const signOut = async () => {
  isDemoAdmin.value = false
  await supabase.auth.signOut()
}

onMounted(async () => {
  document.title = 'Grade Castify'

  const { data: { session } } = await supabase.auth.getSession()
  user.value = session?.user ?? null

  const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user ?? null
  })

  authListener.value = listener
})

onUnmounted(() => {
  authListener.value?.subscription.unsubscribe()
})
</script>

<template>
  <div class="has-background-black-bis" style="min-height: 100vh;">
    <nav class="navbar is-transparent px-5 py-4" role="navigation" aria-label="main navigation">
      <div class="navbar-brand is-align-items-center">
        <a class="navbar-item pl-0">
          <img src="./logo.png" alt="GradeCastify logo" style="max-height: 3rem;" />
        </a>
        <div class="navbar-item pl-0">
          <span class="is-size-3 has-text-primary has-text-weight-semibold">
            GradeCastify
          </span>
        </div>
      </div>

      <div class="navbar-menu is-active">
        <div class="navbar-end">
          <a class="navbar-item has-text-light">Home</a>
          <a class="navbar-item has-text-light" href="group_members.html">Group Members</a>
          <a class="navbar-item has-text-light">Contact Us</a>
        </div>
      </div>
    </nav>

    <section class="section pt-6">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-8 has-text-centered">
            <p class="is-size-6 has-text-grey-light mb-3">Student grade tracking platform</p>
            <h1 class="title is-2 has-text-success mb-4">
              Track and Predict Grades the Right Way
            </h1>
            <p class="subtitle is-5 has-text-grey-light">
              A clean and simple way to monitor performance, stay organized, and plan ahead with confidence.
            </p>
          </div>
        </div>

        <div class="columns is-centered mt-6">
          <div class="column is-8">
            <div class="box has-background-grey-darker">
              <DashboardPanel
                v-if="user || isDemoAdmin"
                :display-name="isDemoAdmin ? 'Demo Admin' : user?.email"
                @sign-out="signOut"
              />

              <div v-else class="p-4">
                <h2 class="title is-3 has-text-white has-text-centered mb-5">Login</h2>

                <div class="field mb-4">
                  <label class="label has-text-light">Email</label>
                  <div class="control">
                    <input
                      class="input"
                      v-model="email"
                      type="email"
                      placeholder="Enter your email"
                    />
                  </div>
                </div>

                <div class="field mb-5">
                  <label class="label has-text-light">Password</label>
                  <div class="control">
                    <input
                      class="input"
                      v-model="password"
                      type="password"
                      placeholder="Enter your password"
                    />
                  </div>
                </div>

                <div class="buttons is-centered">
                  <button class="button is-primary" @click="signIn">
                    Log in
                  </button>
                  <button class="button is-light" @click="signUp">
                    Sign up
                  </button>
                  <button class="button is-link is-light" @click="enterDemoAdmin">
                    Demo Admin
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
