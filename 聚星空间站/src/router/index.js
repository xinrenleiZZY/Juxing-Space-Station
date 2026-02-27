import { createRouter, createWebHashHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import IntellectualPage from '../views/IntellectualPage.vue'
import IAPage from '../views/IAPage.vue'
import Zyzk001Page from '../views/Zyzk001Page.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/intellectual',
    name: 'intellectual',
    component: IntellectualPage
  },
  {
    path: '/ia',
    name: 'ia',
    component: IAPage
  },
  {
    path: '/zyzk001',
    name: 'zyzk001',
    component: Zyzk001Page
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})
// const router = createRouter({
//   history: createWebHashHistory(),
//   routes
// })
export default router
