import { createRouter, createWebHistory } from 'vue-router'
import Search from '../components/Search.vue'
import Login from '@/Login.vue'
import Patient from '@/components/Patient.vue'
import Profilo from '@/components/Profilo.vue'
import Statistiche from '@/components/Statistiche.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/cerca', component: Search },
    { path: '/profilo', component: Profilo },
    { path: '/paziente/:id', component: Patient },
    { path: '/statistiche', component: Statistiche }
  ],
})

export default router
  