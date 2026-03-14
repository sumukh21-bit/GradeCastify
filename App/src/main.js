import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { supabase } from './utils/supabase'

const app = createApp(App)

app.provide('supabase', supabase)
app.mount('#app')
