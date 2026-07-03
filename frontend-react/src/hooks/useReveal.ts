import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'

function revealInViewport(el: Element) {
  const rect = el.getBoundingClientRect()
  const inView =
    rect.top < window.innerHeight &&
    rect.bottom > 0 &&
    rect.left < window.innerWidth &&
    rect.right > 0
  if (inView) {
    el.classList.add('visible')
  }
}

function observeReveals(observer: IntersectionObserver) {
  document.querySelectorAll('.reveal:not(.visible)').forEach((el) => {
    revealInViewport(el)
    observer.observe(el)
  })
}

export function useReveal() {
  const location = useLocation()

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.05, rootMargin: '0px 0px -5% 0px' }
    )

    // Wait for paint, then reveal anything already on screen
    const raf = requestAnimationFrame(() => {
      observeReveals(observer)
      // Fallback for late layout (fonts, WebGL, etc.)
      setTimeout(() => observeReveals(observer), 100)
      setTimeout(() => observeReveals(observer), 500)
    })

    return () => {
      cancelAnimationFrame(raf)
      observer.disconnect()
    }
  }, [location.pathname])
}
