import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import AddCourse from '../views/AddCourse.vue'
import Profile from '../views/Profile.vue'
import EditCourse from '../views/EditCourse.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/add-course', component: AddCourse },
    { path: '/profile', component: Profile },
    { path: '/edit-course/:id', component: EditCourse},
  ],
})
