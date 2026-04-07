import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { supabase } from './utils/supabase'
import router from './router/index.js'

const app = createApp(App)

app.provide('supabase', supabase)
app.use(router)
app.mount('#app')
