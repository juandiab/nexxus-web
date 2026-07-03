import { createBrowserRouter, Navigate } from 'react-router-dom'
import RootLayout from '@/components/layout/RootLayout'
import { ROUTE_SEO } from '@/config/site'
import HomePage from '@/pages/HomePage'
import ServicesPage from '@/pages/ServicesPage'
import ProductsPage from '@/pages/ProductsPage'
import ContactPage from '@/pages/ContactPage'
import ComingSoonPage from '@/pages/ComingSoonPage'

const comingSoon = (key: keyof typeof ROUTE_SEO) => {
  const seo = ROUTE_SEO[key]
  return (
    <ComingSoonPage
      title={seo.title.split(' — ')[0]}
      description={seo.description}
      path={seo.path}
    />
  )
}

export const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      { path: '/', element: <HomePage /> },
      { path: '/services', element: <ServicesPage /> },
      { path: '/products', element: <ProductsPage /> },
      { path: '/contact', element: <ContactPage /> },
      { path: '/about', element: comingSoon('about') },
      { path: '/blog', element: comingSoon('blog') },
      {
        path: '/blog/nsagent-open-source-netscaler-copilot',
        element: <Navigate to="/blog/jpilot-ai-management-platform" replace />,
      },
      { path: '/blog/:slug', element: comingSoon('blog') },
      { path: '/book-demo', element: comingSoon('bookDemo') },
      { path: '/faq', element: comingSoon('faq') },
      { path: '/licensing/activate', element: comingSoon('licensingActivate') },
      { path: '*', element: <Navigate to="/" replace /> },
    ],
  },
])
