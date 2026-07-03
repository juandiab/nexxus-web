import { RouterProvider } from 'react-router-dom'
import { HelmetProvider } from 'react-helmet-async'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { router } from '@/router'

export default function App() {
  return (
    <ErrorBoundary>
      <HelmetProvider>
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:rounded-md focus:bg-[var(--nt-primary)] focus:px-4 focus:py-2 focus:text-white"
        >
          Skip to content
        </a>
        <RouterProvider router={router} />
      </HelmetProvider>
    </ErrorBoundary>
  )
}
