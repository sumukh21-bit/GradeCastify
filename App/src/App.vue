<script setup>
import 'bulma/css/bulma.css'
import { inject, ref, onMounted, onUnmounted } from 'vue'

// set up Supabase client
const supabase = inject('supabase')
const email = ref('')
const password = ref('')
const user = ref(null)
const authListener = ref(null)

// auth functions
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

// auth state listener
onMounted(async () => {
  const { data: { session } } = await supabase.auth.getSession()
  user.value = session?.user ?? null
  console.log(user.value);

  supabase.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user ?? null
  })

})

// Clean up listener on unmount
onUnmounted(() => {
  authListener.value?.subscription.unsubscribe()
})
const demoBTN= async () => {
  user.value = true
}

</script>


<template>
  <!-- route to the dashboard if user is authenticated -->
  <RouterView v-if="user"></RouterView>

  <!-- login/signup form -->
  <div v-else>
    <title>Grade Castify</title>

    <div class="logo-align"><img src="./GCLOGO.png" alt="logo" style="width:70px;height:70px;" ></div>
 

  
  <div class="columns is-centered   ">
   
 
    <div class="columns is-centered " v-if="user">
      
   
    <div class="my-3 py-5 has-text-centered">
      <h1 class="py-3 has-text-centered is-size-6">Hello {{ user.email }}</h1> 
      <button class="py-3 button is-small" @click="signOut">Sign out</button>
    </div>
  </div>
  

  <div class="full-center mb-5" v-else>
     
    <div class="my-3 py-5 has-text-centered">

      <input class="my-3 input  " v-model="email" placeholder="Email" />
      <input class="my-3 input "  v-model="password" type="password" placeholder="Password"></input>
     


      <button class="my-3 mx-2 button  is-fullwidth has-background-white has-text-black mb-4" @click="signIn">Log in</button>
      <button class="my-3 mx-2 button has-background-success has-text-black " @click="signUp">Sign up</button>
    <button class="my-3 mx-2 button " @click="demoBTN">Demo account</button>
      
    </div>
   
  </div>
   

  </div></div>


   
  
  
</template>
