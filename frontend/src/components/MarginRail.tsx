interface MarginRailProps {
  averageRisk: number
  highRiskOpenPRs: number
  flakyTestsWatched: number
  triagedToday: number
}

function riskColor(score: number) {
  if (score >= 70) return 'text-brick'
  if (score >= 40) return 'text-brass'
  return 'text-forest'
}

export default function MarginRail({
  averageRisk,
  highRiskOpenPRs,
  flakyTestsWatched,
  triagedToday,
}: MarginRailProps) {
  return (
    <aside className="border-b border-hairline py-8 lg:w-56 lg:border-b-0 lg:border-r lg:py-0 lg:pr-8">
      <p className="font-sans text-xs uppercase tracking-[0.2em] text-ink-muted">
        Portfolio Risk
      </p>

      <div className="animate-ink-settle mt-3">
        <span className={`font-display text-6xl ${riskColor(averageRisk)}`}>{averageRisk}</span>
        <span className="ml-2 font-sans text-sm text-ink-muted">/ 100 avg.</span>
      </div>

      <div className="mt-2 h-px w-12 bg-brass" aria-hidden="true" />

      <dl className="mt-6 space-y-4 font-sans text-sm">
        {[
          { label: 'High-risk PRs open', value: highRiskOpenPRs, tone: 'text-brick' },
          { label: 'Flaky tests watched', value: flakyTestsWatched, tone: 'text-ink' },
          { label: 'Triaged today', value: triagedToday, tone: 'text-ink' },
        ].map((item, i) => (
          <div
            key={item.label}
            className="animate-ink-settle flex items-baseline justify-between gap-4 lg:flex-col lg:items-start lg:gap-1"
            style={{ animationDelay: `${120 + i * 80}ms` }}
          >
            <dt className="text-ink-muted">{item.label}</dt>
            <dd className={`font-mono tabular text-base ${item.tone}`}>{item.value}</dd>
          </div>
        ))}
      </dl>
    </aside>
  )
}
