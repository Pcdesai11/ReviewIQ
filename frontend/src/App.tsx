import { useEffect } from 'react'
import type { ReactNode } from 'react'
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import DashboardPage from './pages/DashboardPage'
import SakuraBackground from './components/SakuraBackground'

function ScrollToTop() {
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return null
}

function PageTransition({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()

  return (
    <div key={pathname} className="animate-page-enter">
      {children}
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <SakuraBackground />
      <ScrollToTop />
      <PageTransition>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </PageTransition>
    </BrowserRouter>
  )
}
