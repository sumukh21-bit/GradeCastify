<script setup>
import 'bulma/css/bulma.css'
import { inject, ref, onMounted, onUnmounted } from 'vue'

const supabase = inject('supabase')
const email = ref('')
const password = ref('')
const user = ref(null)
const authListener = ref(null)

const signIn = async () => {
  await supabase.auth.signInWithPassword({ email: email.value, password: password.value })
  email.value = ''
  password.value = ''
}

const signUp = async () => {
  await supabase.auth.signUp({ email: email.value, password: password.value })
  email.value = ''
  password.value = ''
}

const signOut = async () => {
  await supabase.auth.signOut()
}

onMounted(async () => {
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
  <h1 class="pt-6 pb-1 has-text-centered is-size-4 has-text-primary">
    GradeCastify
  </h1>
  <div class="columns is-centered" v-if="user">
    <div class="my-3 py-5 has-text-centered">
      <h1 class="py-3 has-text-centered is-size-6">Hello {{ user.email }}</h1> 
      <button class="py-3 button is-small" @click="signOut">Sign out</button>
    </div>
  </div>

  <div class="columns is-centered" v-else>
    <div class="my-3 py-5 has-text-centered">
      <input class="my-3 input is-small" v-model="email" placeholder="email" />
      <input class="my-3 input is-small" v-model="password" type="password" placeholder="password" />
      <button class="my-3 mx-2 button is-small" @click="signIn">Log in</button>
      <button class="my-3 mx-2 button is-small" @click="signUp">Sign up</button>
    </div>
  </div>
</template>
