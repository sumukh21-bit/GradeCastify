<script setup>
import { inject } from 'vue'
import { useRouter } from 'vue-router'
import logo from '../logo.png'

const supabase = inject('supabase')
const router = useRouter()

const handleSignOut = async () => {
  if (supabase) {
    await supabase.auth.signOut()
  }
  router.push('/')
}
</script>

<template>
  <aside class="menu p-4 gc-sidebar is-flex is-flex-direction-column is-justify-content-space-between">
    <div>
      <div class="is-flex is-align-items-center mb-5">
        <img :src="logo" alt="GradeCastify logo" style="width: 42px; height: 42px;" />
        <div class="ml-3">
          <p class="has-text-weight-bold is-size-5 has-text-white mb-1">GradeCastify</p>
          <p class="is-size-7 has-text-grey-light">Student Dashboard</p>
        </div>
      </div>

      <p class="menu-label has-text-grey-light">Workspace</p>
      <ul class="menu-list">
        <li><router-link to="/dashboard" class="has-text-white">Dashboard</router-link></li>
        <li><router-link to="/add-course" class="has-text-white">Add Course</router-link></li>
        <li><a href="/group_members.html" class="has-text-white">Group Member</a></li>
      </ul>
    </div>

    <div>
      <div class="box gc-soft-box mb-3">
        <p class="has-text-weight-semibold has-text-white">Demo Admin</p>
        <p class="is-size-7 has-text-grey-light">Testing Account</p>
      </div>

      <button class="button is-fullwidth gc-accent-btn has-text-weight-semibold" @click="handleSignOut">
        Sign out
      </button>
    </div>
  </aside>
</template>
