import { createRouter, createWebHistory } from 'vue-router'
import ActivateView from '@/views/ActivateView.vue'

const router = createRouter({
  history: createWebHistory('/licensing/'),
  routes: [
    {
      path: '/activate',
      name: 'activate',
      component: ActivateView,
      meta: { title: 'License activation' },
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: { name: 'activate' },
    },
  ],
})

router.afterEach((to) => {
  document.title = to.meta.title
    ? `${to.meta.title} · Nexxus Tech`
    : 'License activation · Nexxus Tech'
})

export default router
