import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="border-b border-hairline bg-ivory/75 backdrop-blur-sm">
      <div className="mx-auto flex max-w-6xl items-baseline justify-between px-6 py-5 sm:px-10">
        <div className="flex items-baseline gap-3">
          <Link
            to="/"
            className="font-display text-2xl italic tracking-tight text-navy transition-opacity duration-300 hover:opacity-80"
          >
            ReviewIQ
          </Link>
          <span className="hidden font-sans text-xs uppercase tracking-[0.2em] text-ink-muted sm:inline">
            Code Review & CI Triage
          </span>
        </div>

        <nav className="flex items-center gap-6 font-sans text-sm text-ink-muted">
          <a href="#pulls" className="transition-colors duration-300 hover:text-ink">
            Pull Requests
          </a>
          <a href="#flaky" className="transition-colors duration-300 hover:text-ink">
            Flaky Tests
          </a>
          <a href="#triage" className="transition-colors duration-300 hover:text-ink">
            Triage
          </a>
          <Link
            to="/"
            className="hidden font-sans text-xs text-ink-muted transition-colors duration-300 hover:text-ink sm:inline"
          >
            Home
          </Link>
          <span className="hidden font-mono text-xs text-ink-muted lg:inline">
            platform/* &middot; main
          </span>
        </nav>
      </div>
    </header>
  )
}
