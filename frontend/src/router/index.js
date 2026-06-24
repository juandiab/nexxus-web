import { createRouter, createWebHistory } from 'vue-router'
import { ROUTE_SEO } from '@/config/site.js'
import { applySeo } from '@/utils/seo.js'
import { jsonLdForRoute } from '@/data/structuredData.js'
import HomeView from '@/views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { seo: ROUTE_SEO.home }
  },
  {
    path: '/services',
    name: 'services',
    component: () => import('@/views/ServicesView.vue'),
    meta: { seo: ROUTE_SEO.services }
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('@/views/ProductsView.vue'),
    meta: { seo: ROUTE_SEO.products }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
    meta: { seo: ROUTE_SEO.about }
  },
  {
    path: '/blog',
    name: 'blog',
    component: () => import('@/views/BlogView.vue'),
    meta: { seo: ROUTE_SEO.blog }
  },
  {
    path: '/blog/nsagent-open-source-netscaler-copilot',
    redirect: '/blog/jpilot-ai-management-platform',
  },
  {
    path: '/blog/:slug',
    name: 'blog-post',
    component: () => import('@/views/BlogPostView.vue'),
    meta: { seo: ROUTE_SEO.blog, dynamic: true }
  },
  {
    path: '/contact',
    name: 'contact',
    component: () => import('@/views/ContactView.vue'),
    meta: { seo: ROUTE_SEO.contact }
  },
  {
    path: '/book-demo',
    name: 'book-demo',
    component: () => import('@/views/BookDemoView.vue'),
    meta: { seo: ROUTE_SEO.bookDemo }
  },
  {
    path: '/faq',
    name: 'faq',
    component: () => import('@/views/FaqView.vue'),
    meta: { seo: ROUTE_SEO.faq }
  },
  {
    path: '/licensing/activate',
    name: 'licensing-activate',
    component: () => import('@/views/LicensingActivateView.vue'),
    meta: { seo: ROUTE_SEO.licensingActivate }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  }
})

router.afterEach((to) => {
  if (to.meta.dynamic) return

  const seo = to.meta.seo
  if (!seo) return

  applySeo({
    title: seo.title,
    description: seo.description,
    path: seo.path,
    image: seo.image,
    imageAlt: seo.imageAlt,
    noindex: seo.noindex,
    type: 'website',
    jsonLd: jsonLdForRoute(to.name),
  })
})

export default router
