import { Link } from 'react-router-dom'
import FadeIn from '../components/FadeIn'
import { useLandingPreview } from '../hooks/useDashboardData'

const features = [
  {
    title: 'Risk-ranked pull requests',
    description:
      'Every open PR scored and sorted — high-risk changes surface first, with rationale attached.',
    accent: 'text-navy',
  },
  {
    title: 'Flaky test watch',
    description:
      'Tests that fail intermittently are flagged before they burn another CI cycle.',
    accent: 'text-forest',
  },
  {
    title: 'CI triage queue',
    description:
      'Failures classified as regression, flake, infra, or environment — explained, not just logged.',
    accent: 'text-brass',
  },
]

export default function LandingPage() {
  const { portfolioSummary, topPull, isLoading } = useLandingPreview()

  return (
    <div className="relative min-h-screen">
      <header className="border-b border-hairline bg-ivory/75 backdrop-blur-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5 sm:px-10">
          <Link
            to="/"
            className="font-display text-2xl italic tracking-tight text-navy transition-opacity duration-300 hover:opacity-80"
          >
            ReviewIQ
          </Link>
          <Link
            to="/dashboard"
            className="rounded-sm border border-hairline bg-cream px-4 py-2 font-sans text-sm text-ink transition-all duration-300 hover:border-brass hover:bg-brass/5"
          >
            Open Dashboard
          </Link>
        </div>
      </header>

      <main>
        {/* Hero */}
        <section className="relative overflow-hidden border-b border-hairline">
          <div className="relative mx-auto max-w-6xl px-6 pb-20 pt-16 sm:px-10 sm:pb-28 sm:pt-24">
            <p className="animate-fade-up is-visible font-sans text-xs uppercase tracking-[0.25em] text-ink-muted">
              Code review &amp; CI triage
            </p>

            <h1
              className="animate-fade-up is-visible mt-4 max-w-3xl font-display text-4xl leading-tight text-ink sm:text-5xl lg:text-6xl"
              style={{ animationDelay: '80ms' }}
            >
              Know what to review{' '}
              <span className="italic text-navy">before</span> CI breaks.
            </h1>

            <p
              className="animate-fade-up is-visible mt-6 max-w-xl font-sans text-base leading-relaxed text-ink-muted sm:text-lg"
              style={{ animationDelay: '160ms' }}
            >
              ReviewIQ ranks pull requests by risk, watches for flaky tests, and triages CI failures
              — so your team spends time fixing, not guessing.
            </p>

            <div
              className="animate-fade-up is-visible mt-10 flex flex-wrap items-center gap-4"
              style={{ animationDelay: '240ms' }}
            >
              <Link
                to="/dashboard"
                className="group inline-flex items-center gap-2 rounded-sm bg-navy px-6 py-3 font-sans text-sm font-medium text-cream transition-all duration-300 hover:bg-navy/90 hover:shadow-lg hover:shadow-navy/10"
              >
                View live dashboard
                <span className="inline-block transition-transform duration-300 group-hover:translate-x-1">
                  →
                </span>
              </Link>
              <a
                href="#features"
                className="font-sans text-sm text-ink-muted transition-colors duration-300 hover:text-ink"
              >
                See how it works
              </a>
            </div>

            {/* Live preview card */}
            <div
              className="animate-fade-up is-visible mt-16 rounded-sm border border-hairline bg-cream/80 p-6 backdrop-blur-sm sm:p-8"
              style={{ animationDelay: '360ms' }}
            >
              <div className="flex items-baseline justify-between gap-4 border-b border-hairline pb-4">
                <div>
                  <p className="font-sans text-xs uppercase tracking-[0.2em] text-ink-muted">
                    Portfolio snapshot
                  </p>
                  <p className="mt-1 font-display text-lg text-ink">
                    {isLoading ? 'Loading…' : 'Live from Results API'}
                  </p>
                </div>
                <div className="text-right">
                  <span className="font-display text-4xl text-brass">
                    {portfolioSummary?.averageRisk ?? '—'}
                  </span>
                  <span className="ml-1 font-sans text-sm text-ink-muted">/ 100 avg risk</span>
                </div>
              </div>

              <div className="mt-4 grid gap-4 sm:grid-cols-3">
                {[
                  { label: 'High-risk PRs', value: portfolioSummary?.highRiskOpenPRs, tone: 'text-brick' },
                  { label: 'Flaky tests', value: portfolioSummary?.flakyTestsWatched, tone: 'text-ink' },
                  { label: 'Triaged today', value: portfolioSummary?.triagedToday, tone: 'text-forest' },
                ].map((stat) => (
                  <div key={stat.label} className="rounded-sm border border-hairline/60 bg-ivory px-4 py-3">
                    <p className="font-sans text-xs text-ink-muted">{stat.label}</p>
                    <p className={`mt-1 font-mono tabular text-2xl ${stat.tone}`}>
                      {stat.value ?? '—'}
                    </p>
                  </div>
                ))}
              </div>

              {topPull && (
                <div className="mt-4 flex items-center justify-between gap-4 border-t border-hairline/70 pt-4 transition-colors duration-300 hover:bg-ivory/60">
                  <div className="min-w-0">
                    <p className="truncate font-sans text-sm font-medium text-ink">
                      {topPull.id} · {topPull.title}
                    </p>
                    <p className="mt-0.5 truncate font-sans text-xs text-ink-muted">
                      {topPull.repo} · {topPull.rationale}
                    </p>
                  </div>
                  <div className="shrink-0 text-right">
                    <span className="font-mono tabular text-base text-brick">{topPull.riskScore}</span>
                    <p className="font-sans text-[11px] uppercase tracking-wide text-ink-muted">
                      risk score
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="border-b border-hairline py-20 sm:py-28">
          <div className="mx-auto max-w-6xl px-6 sm:px-10">
            <FadeIn>
              <p className="font-sans text-xs uppercase tracking-[0.25em] text-ink-muted">
                How ReviewIQ works
              </p>
              <h2 className="mt-3 max-w-lg font-display text-3xl text-ink sm:text-4xl">
                One view for everything that needs attention.
              </h2>
            </FadeIn>

            <div className="mt-14 grid gap-8 sm:grid-cols-3">
              {features.map((feature, i) => (
                <FadeIn key={feature.title} delay={i * 100}>
                  <article className="group h-full rounded-sm border border-hairline bg-cream/50 p-6 transition-all duration-500 hover:-translate-y-1 hover:border-brass/40 hover:bg-cream hover:shadow-md hover:shadow-brass/5">
                    <div className={`mb-4 h-px w-8 bg-current ${feature.accent} transition-all duration-500 group-hover:w-12`} />
                    <h3 className={`font-display text-xl ${feature.accent}`}>{feature.title}</h3>
                    <p className="mt-3 font-sans text-sm leading-relaxed text-ink-muted">
                      {feature.description}
                    </p>
                  </article>
                </FadeIn>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-20 sm:py-28">
          <div className="mx-auto max-w-6xl px-6 text-center sm:px-10">
            <FadeIn>
              <h2 className="font-display text-3xl text-ink sm:text-4xl">
                Ready to see the full dashboard?
              </h2>
              <p className="mx-auto mt-4 max-w-md font-sans text-sm leading-relaxed text-ink-muted">
                Explore pull request risk scores, flaky test alerts, and the CI triage queue — powered
                by the ReviewIQ Results API.
              </p>
              <Link
                to="/dashboard"
                className="mt-8 inline-flex items-center gap-2 rounded-sm border border-navy bg-navy px-8 py-3 font-sans text-sm font-medium text-cream transition-all duration-300 hover:bg-navy/90 hover:shadow-lg hover:shadow-navy/10"
              >
                Open Dashboard
                <span aria-hidden="true">→</span>
              </Link>
            </FadeIn>
          </div>
        </section>
      </main>

      <footer className="border-t border-hairline bg-ivory/75 backdrop-blur-sm">
        <div className="mx-auto max-w-6xl px-6 py-6 font-sans text-xs text-ink-muted sm:px-10">
          ReviewIQ — connected to the Results API.
        </div>
      </footer>
    </div>
  )
}
