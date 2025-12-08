import { createRouter, createWebHistory } from 'vue-router'
import Calendar from '../views/calendar.vue'
import AdminPanel from '../views/adminpanel.vue'
import login from '../views/login.vue'

const routes = [
  {
    path: '/',
    name: 'Calendar',
    component: Calendar
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: AdminPanel
  },
  {
    path: '/login',
    name: 'Login',
    component: login
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
