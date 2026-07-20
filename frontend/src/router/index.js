import { createRouter, createWebHistory } from 'vue-router'
import Search from '../components/Search.vue'
import Login from '@/Login.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Login },
    { path: '/user/:username', component: Search },
  ],
})

export default router
  