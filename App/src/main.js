import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { supabase } from './utils/supabase'
import router from './router'

const app = createApp(App)

app.use(router)
app.provide('supabase', supabase)
app.mount('#app')
