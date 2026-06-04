import { createRouter, createWebHistory } from 'vue-router'
import { useAdminAuth } from '@/composables/useAdminAuth'

const routes = [
  {
    path: '/',
    redirect: { name: 'dashboard' },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true, title: 'Sign in' },
  },
  {
    path: '/setup',
    name: 'setup',
    component: () => import('@/views/SetupView.vue'),
    meta: { requiresAuth: true, title: 'Account setup' },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true, requiresSetup: true, title: 'Dashboard' },
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('@/views/UsersView.vue'),
    meta: { requiresAuth: true, requiresSetup: true, requiresAdmin: true, title: 'Users' },
  },
  {
    path: '/licensing',
    name: 'licensing',
    component: () => import('@/views/LicensingView.vue'),
    meta: {
      requiresAuth: true,
      requiresSetup: true,
      requiresRole: ['admin', 'licensing'],
      title: 'Licensing',
    },
  },
  {
    path: '/blogs',
    name: 'blogs',
    component: () => import('@/views/InProgressView.vue'),
    meta: {
      requiresAuth: true,
      requiresSetup: true,
      requiresRole: ['admin', 'blog'],
      title: 'Blogs',
      sectionTitle: 'Blogs',
      sectionSubtitle: 'Create and publish blog posts.',
    },
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/InProgressView.vue'),
    meta: {
      requiresAuth: true,
      requiresSetup: true,
      requiresAdmin: true,
      title: 'Settings',
      sectionTitle: 'Settings',
      sectionSubtitle: 'Configure admin console preferences.',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: { name: 'dashboard' },
  },
]

const router = createRouter({
  history: createWebHistory('/adminconsole/'),
  routes,
})

router.beforeEach(async (to) => {
  const { isAuthenticated, validateSession, setupComplete, isAdmin, user, refreshUser } =
    useAdminAuth()

  if (to.meta.requiresAuth) {
    if (!isAuthenticated.value) {
      const ok = await validateSession()
      if (!ok) return { name: 'login', query: { redirect: to.fullPath } }
    } else {
      await refreshUser()
    }

    if (!setupComplete.value && to.name !== 'setup') {
      return { name: 'setup' }
    }

    if (setupComplete.value && to.name === 'setup') {
      return { name: 'dashboard' }
    }

    if (to.meta.requiresSetup && !setupComplete.value) {
      return { name: 'setup' }
    }

    if (to.meta.requiresAdmin && !isAdmin.value) {
      return { name: 'dashboard' }
    }

    if (to.meta.requiresRole?.length) {
      const role = user.value?.role
      if (!role || !to.meta.requiresRole.includes(role)) {
        return { name: 'dashboard' }
      }
    }

    return true
  }

  if (to.meta.guest) {
    if (isAuthenticated.value || (await validateSession())) {
      if (!setupComplete.value) return { name: 'setup' }
      return { name: 'dashboard' }
    }
  }

  return true
})

router.afterEach((to) => {
  const base = 'Nexxus Tech — Admin Console'
  document.title = to.meta.title ? `${to.meta.title} · ${base}` : base
})

export default router
