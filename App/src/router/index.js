import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../Pages/HomePage.vue'
import DashboardPage from '../Pages/DashboardPage.vue'
import AddCoursePage from '../Pages/AddCoursePage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage
  },
  {
    path: '/add-course',
    name: 'add-course',
    component: AddCoursePage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
