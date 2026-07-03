import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { SeoHead } from '@/components/SeoHead'

interface ComingSoonPageProps {
  title: string
  description: string
  path: string
}

export default function ComingSoonPage({ title, description, path }: ComingSoonPageProps) {
  return (
    <div className="flex min-h-[70vh] items-center justify-center pt-24">
      <SeoHead title={title} description={description} path={path} />
      <div className="container text-center">
        <span className="section-label">Coming Soon</span>
        <h1 className="mb-4">{title}</h1>
        <p className="mx-auto mb-8 max-w-md text-[var(--nt-text-muted)]">{description}</p>
        <Link to="/" className="btn btn-primary">
          <ArrowLeft className="h-4 w-4" /> Back to Home
        </Link>
      </div>
    </div>
  )
}
