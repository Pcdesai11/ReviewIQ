import Header from '../components/Header'
import MarginRail from '../components/MarginRail'
import ReviewSection, { type ReviewRow, type Tone } from '../components/ReviewSection'
import FadeIn from '../components/FadeIn'
import DataStatus from '../components/DataStatus'
import { useDashboardData } from '../hooks/useDashboardData'
import type { TriageClass } from '../api/types'

function scoreTone(score: number): Tone {
  if (score >= 70) return 'high'
  if (score >= 40) return 'mid'
  return 'low'
}

function confidenceTone(confidence: number): Tone {
  if (confidence >= 70) return 'high'
  if (confidence >= 40) return 'mid'
  return 'low'
}

const triageTagTone: Record<TriageClass, Tone> = {
  regression: 'high',
  flaky: 'mid',
  infra: 'neutral',
  environment: 'low',
}

function formatMinutesAgo(minutes: number) {
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.round(minutes / 60)
  return `${hours}h ago`
}

export default function DashboardPage() {
  const { metrics, pulls, flakyTests, triageItems, isLoading, isError, error, refetch } =
    useDashboardData()

  const pullRequestRows: ReviewRow[] = pulls.map((pr) => ({
    id: pr.id,
    primary: `${pr.id} · ${pr.title}`,
    secondary: `${pr.repo} · ${pr.author} · ${pr.filesChanged} files changed · ${pr.rationale}`,
    value: String(pr.riskScore),
    valueLabel: 'risk score',
    valueTone: scoreTone(pr.riskScore),
  }))

  const flakyTestRows: ReviewRow[] = flakyTests.map((test) => ({
    id: test.id,
    primary: test.name,
    secondary: `${test.suite} · last flaked ${test.lastFlaked}`,
    value: `${test.confidence}%`,
    valueLabel: 'confidence',
    valueTone: confidenceTone(test.confidence),
  }))

  const triageRows: ReviewRow[] = triageItems.map((item) => ({
    id: item.id,
    primary: item.run,
    secondary: `${item.commit} · ${item.summary}`,
    tagLabel: item.classification,
    tagTone: triageTagTone[item.classification],
    value: formatMinutesAgo(item.minutesAgo),
    valueLabel: 'reported',
    valueTone: 'neutral',
  }))

  const showContent = !isLoading && !isError && metrics

  return (
    <div className="relative min-h-screen">
      <Header />

      <DataStatus
        isLoading={isLoading}
        isError={isError}
        error={error}
        onRetry={() => void refetch()}
      />

      {showContent && (
        <main className="mx-auto max-w-6xl px-6 sm:px-10">
          <div className="flex flex-col lg:flex-row lg:gap-10">
            <FadeIn delay={80}>
              <MarginRail
                averageRisk={metrics.averageRisk}
                highRiskOpenPRs={metrics.highRiskOpenPRs}
                flakyTestsWatched={metrics.flakyTestsWatched}
                triagedToday={metrics.triagedToday}
              />
            </FadeIn>

            <div className="flex-1 divide-y divide-hairline lg:pl-2">
              <FadeIn delay={160}>
                <ReviewSection
                  id="pulls"
                  eyebrow="Open Pull Requests"
                  description="Sorted by risk, highest first"
                  rows={pullRequestRows}
                  emptyState="No open pull requests right now."
                />
              </FadeIn>

              <FadeIn delay={240}>
                <ReviewSection
                  id="flaky"
                  eyebrow="Flaky Test Watch"
                  description="Tests flagged before they waste a re-run"
                  rows={flakyTestRows}
                  emptyState="No tests are currently flagged as flake-risk."
                />
              </FadeIn>

              <FadeIn delay={320}>
                <ReviewSection
                  id="triage"
                  eyebrow="CI Triage Queue"
                  description="Recent failures, classified and explained"
                  rows={triageRows}
                  emptyState="No CI failures to triage."
                />
              </FadeIn>
            </div>
          </div>
        </main>
      )}

      <footer className="border-t border-hairline bg-ivory/75 backdrop-blur-sm">
        <div className="mx-auto max-w-6xl px-6 py-6 font-sans text-xs text-ink-muted sm:px-10">
          ReviewIQ dashboard — live data from the Results API. No GitHub repositories connected
          yet.
        </div>
      </footer>
    </div>
  )
}
