<script setup>
import 'bulma/css/bulma.css'
import { inject, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const supabase = inject('supabase')
const router = useRouter()

const email = ref('')
const password = ref('')
const user = ref(null)
const authListener = ref(null)

const signIn = async () => {
  localStorage.removeItem('gc_demo_admin')

  const { error } = await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value
  })

  if (!error) {
    email.value = ''
    password.value = ''
    router.push('/dashboard')
  }
}

const signUp = async () => {
  localStorage.removeItem('gc_demo_admin')

  const { error } = await supabase.auth.signUp({
    email: email.value,
    password: password.value
  })

  if (!error) {
    email.value = ''
    password.value = ''
    router.push('/dashboard')
  }
}

const enterDemoAdmin = () => {
  localStorage.setItem('gc_demo_admin', 'true')
  router.push('/dashboard')
}

onMounted(async () => {
  document.title = 'Grade Castify'

  const { data: { session } } = await supabase.auth.getSession()
  user.value = session?.user ?? null

  if (user.value) {
    localStorage.removeItem('gc_demo_admin')
    router.push('/dashboard')
  }

  const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user ?? null

    if (session?.user) {
      localStorage.removeItem('gc_demo_admin')
    }
  })

  authListener.value = listener
})

onUnmounted(() => {
  authListener.value?.subscription.unsubscribe()
})
</script>

<template>
  <section class="section gc-home-section">
    <div class="container">
        <div class="columns is-centered">
        <div class="column is-8 has-text-centered gc-home-hero">
            <p class="gc-home-eyebrow mb-3">Student grade tracking platform</p>

            <h1 class="title is-2 gc-home-title mb-4">
            Track and Predict Grades the Right Way
            </h1>

            <p class="subtitle is-5 gc-home-subtitle">
            A clean and simple way to monitor performance, stay organized, and plan ahead with confidence.
            </p>
        </div>
        </div>

        <div class="columns is-centered gc-home-login-row">
        <div class="column is-6">
            <div class="box has-background-grey-darker p-5 gc-login-box">
            <h2 class="title is-3 has-text-white has-text-centered mb-5">Login</h2>

            <div class="field">
                <label class="label gc-login-label">Email</label>
                <div class="control">
                <input
                    class="input gc-login-input"
                    type="email"
                    v-model="email"
                    placeholder="Enter your email"
                />
                </div>
            </div>

            <div class="field">
                <label class="label gc-login-label">Password</label>
                <div class="control">
                <input
                    class="input gc-login-input"
                    type="password"
                    v-model="password"
                    placeholder="Enter your password"
                />
                </div>
            </div>

            <div class="buttons is-centered mt-5">
                <button class="button gc-accent-btn" @click="signIn">Log in</button>
                <button class="button gc-secondary-btn" @click="signUp">Sign up</button>
                <button class="button gc-ghost-btn" @click="enterDemoAdmin">Demo Admin</button>
            </div>
            </div>
        </div>
        </div>
    </div>
    </section>
</template>
