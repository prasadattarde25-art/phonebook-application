import { createRouter, createWebHistory } from 'vue-router'
import ContactList from '../components/ContactList.vue'
import ContactDetail from '../ContactDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: ContactList
  },
  {
    path: '/contact/:id',
    name: 'ContactDetail',
    component: ContactDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router