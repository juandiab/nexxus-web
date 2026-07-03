import { Outlet } from 'react-router-dom'
import NavBar from '@/components/layout/NavBar'
import AppFooter from '@/components/layout/AppFooter'
import { Toaster } from '@/components/ui/sonner'
import { useReveal } from '@/hooks/useReveal'

export default function RootLayout() {
  useReveal()
  return (
    <>
      <NavBar />
      <main id="main-content" className="min-h-screen">
        <Outlet />
      </main>
      <AppFooter />
      <Toaster />
    </>
  )
}
