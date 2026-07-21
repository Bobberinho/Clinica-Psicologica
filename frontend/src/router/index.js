import { createRouter, createWebHistory } from 'vue-router'
import Search from '../components/Search.vue'
import Login from '@/Login.vue'
import Patient from '@/components/Patient.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Login },
    { path: '/user/:username', component: Search },
    { path: '/patient/:id', component: Patient },
  ],
})

export default router
  