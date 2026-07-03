import { Component, type ErrorInfo, type ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null }

  static getDerivedStateFromError(error: Error) {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('App render error:', error, info)
  }

  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 24, color: '#f0f0f0', background: '#1c1c1e', minHeight: '100vh' }}>
          <h1 style={{ color: '#00a8e0', marginBottom: 16 }}>Something went wrong</h1>
          <pre style={{ whiteSpace: 'pre-wrap', color: '#ff6b6b' }}>{this.state.error.message}</pre>
        </div>
      )
    }
    return this.props.children
  }
}
