<script setup>
import 'bulma/css/bulma.css'
import { inject, ref, onMounted, onUnmounted } from 'vue'

const supabase = inject('supabase')
const email = ref('')
const password = ref('')
const user = ref(null)
const authListener = ref(null)

const refreshAuthState = async () => {
  const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

  if (isDemoAdmin) {
    user.value = { email: 'demo@gradecastify.local' }
    return
  }

  const { data: { session } } = await supabase.auth.getSession()
  user.value = session?.user ?? null
}

const signIn = async () => {
  localStorage.removeItem('gc_demo_admin')
  await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value
  })
  email.value = ''
  password.value = ''
  await refreshAuthState()
}

const signUp = async () => {
  localStorage.removeItem('gc_demo_admin')
  await supabase.auth.signUp({
    email: email.value,
    password: password.value
  })
  email.value = ''
  password.value = ''
  await refreshAuthState()
}

const signOut = async () => {
  localStorage.removeItem('gc_demo_admin')
  await supabase.auth.signOut()
  user.value = null
  window.location.href = '/'
}

const demoBTN = async () => {
  localStorage.setItem('gc_demo_admin', 'true')
  user.value = { email: 'demo@gradecastify.local' }
}

onMounted(async () => {
  await refreshAuthState()

  authListener.value = supabase.auth.onAuthStateChange(async (_event, session) => {
    const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

    if (isDemoAdmin) {
      user.value = { email: 'demo@gradecastify.local' }
      return
    }

    user.value = session?.user ?? null
  })
})

onUnmounted(() => {
  if (authListener.value?.data?.subscription) {
    authListener.value.data.subscription.unsubscribe()
  }
})
</script>

<template>
  <RouterView v-if="user" />

  <div v-else>
    <title>Grade Castify</title>

    <div class="logo-align">
      <img src="./GCLOGO.png" alt="logo" style="width:70px;height:70px;">
    </div>

    <div class="columns is-centered">
      <div class="full-center mb-5">
        <div class="my-3 py-5 has-text-centered">
          <input class="my-3 input" v-model="email" placeholder="Email" />
          <input class="my-3 input" v-model="password" type="password" placeholder="Password" />

          <button class="my-3 mx-2 button is-fullwidth has-background-white has-text-black mb-4" @click="signIn">
            Log in
          </button>

          <button class="my-3 mx-2 button has-background-success has-text-black" @click="signUp">
            Sign up
          </button>

          <button class="my-3 mx-2 button" @click="demoBTN">
            Demo account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>