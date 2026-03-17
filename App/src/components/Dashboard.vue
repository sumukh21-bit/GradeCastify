<script setup>
import { inject, ref, onMounted } from 'vue'


const supabase = inject('supabase')
const displayName = ref('User')

onMounted(async () => {
  const isDemoAdmin = localStorage.getItem('gc_demo_admin') === 'true'

  if (isDemoAdmin) {
    displayName.value = 'Demo Admin'
    return
  }

  const { data: { session } } = await supabase.auth.getSession()

  if (session?.user?.email) {
    displayName.value = session.user.email
  } else {
    displayName.value = 'User'
  }
})
</script>

<template >
     <nav>
      
      <div class="navbar-end">
        <nav class="navbar-start title">Grade<h1 class="has-text-success title">Castify</h1></nav>
      <a class="is-size-6 navbar-item">
        Sign out
      </a>
      <a class="is-size-6 navbar-item is-rounded" href="group_members.html">
        <button class="has-background-white">{{ displayName }}</button>
      </a>
      
    </div>

     </nav>
  <div>
 
       <h1 class="title is-size-2 has-text-success has-text-centered mt-6">Dashboard</h1>
    

  </div>
 
  <div class="mainContainer  mt-4 columns is-centered">
    
    <div class="  column is-2">
      <div class="box">
        <h1 class="is-size-8">Current Average</h1>
       <h2 class="is-size-3">0</h2></div>
       
    </div>
    <div class="  column is-2">
      <div class="box">
        <h1 class="is-size-8">Predicted Average</h1>
       <h2 class="is-size-3">0</h2></div>
       
    </div>
    <div class="  column is-2">
      <div class="box"> 
        <h1 class="is-size-8">Courses Taken</h1>
       <h2 class="is-size-3">0</h2></div>
      
    </div>
  </div>

  <div class="Courses px-6 column is-8">
    <h1 class="title px-6 has-text-centered">My Courses <button class="navbar-end mb-6">+ Add</button></h1>
    

  </div>
</template> 