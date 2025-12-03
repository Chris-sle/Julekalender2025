import { createRouter, createWebHistory } from 'vue-router'
import Calendar from '../views/Calendar.vue'
import AdminPanel from '../views/adminpanel.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
