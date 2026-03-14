<script setup>
import 'bulma/css/bulma.css'
import { inject, ref, onMounted, onUnmounted } from 'vue'
import Dashboard from './components/Dashboard.vue'


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
  console.log(user.value);

  supabase.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user ?? null
  })

})

onUnmounted(() => {
  authListener.value?.subscription.unsubscribe()
})
const demoBTN= async () => {
  user.value = true
}

</script>


<template>
  <Dashboard v-if="user"></Dashboard>

  <div v-else>
    <title>Grade Castify</title>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <img src="./logo.png" alt="logo" width="50">
   <div class="navbar-start is-size-4 has-text-primary">
        GradeCastify

   </div>


       <div class="navbar-end">
      <a class="is-size-6 navbar-item">
        Home
      </a>
      <a class="is-size-6 navbar-item" href="group_members.html">
        Group Members
      </a>
      <a class="is-size-6 navbar-item">
        Contact Us
      </a>
    </div>
   


  </nav>
   <h1 class="has-text-centered is-size-4 has-text-success mt-6">Track and Predict Grades the right way</h1>
  
  <div class="columns is-centered mt-6  ">
   
    <div class="l-container  box column is-4 has-background-grey-darker  ">
    
    <div class="columns is-centered " v-if="user">
    <div class="my-3 py-5 has-text-centered">
      <h1 class="py-3 has-text-centered is-size-6">Hello {{ user.email }}</h1> 
      <button class="py-3 button is-small" @click="signOut">Sign out</button>
    </div>
  </div>

  <div class="columns is-centered" v-else>
    <div class="my-3 py-5 has-text-centered">
      <h1 class="is-size-4 has-text-black">Login</h1>
      <input class="my-3 input is-small" v-model="email" placeholder="email" />
      <input class="my-3 input is-small" v-model="password" type="password" placeholder="password" />
      <button class="my-3 mx-2 button is-small" @click="signIn">Log in</button>
      <button class="my-3 mx-2 button is-small" @click="signUp">Sign up</button>
      <button class="my-3 mx-2 button is-small" @click="demoBTN">Demo account</button>
    </div>
  </div>

  </div></div>

  </div>
   
  
  
</template>
