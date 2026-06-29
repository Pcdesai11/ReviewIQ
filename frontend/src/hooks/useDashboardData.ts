import { useQueries } from '@tanstack/react-query'
import { api } from '../api/client'

export function useDashboardData() {
  const results = useQueries({
    queries: [
      {
        queryKey: ['metrics', 'summary'],
        queryFn: api.getMetricsSummary,
      },
      {
        queryKey: ['pulls'],
        queryFn: api.getPulls,
      },
      {
        queryKey: ['tests', 'flaky'],
        queryFn: api.getFlakyTests,
      },
      {
        queryKey: ['ci-runs', 'triage'],
        queryFn: api.getTriageQueue,
      },
    ],
  })

  const [metrics, pulls, flakyTests, triageItems] = results

  const isLoading = results.some((r) => r.isLoading)
  const isError = results.some((r) => r.isError)
  const error = results.find((r) => r.error)?.error ?? null

  return {
    metrics: metrics.data,
    pulls: pulls.data ?? [],
    flakyTests: flakyTests.data ?? [],
    triageItems: triageItems.data ?? [],
    isLoading,
    isError,
    error,
    refetch: () => Promise.all(results.map((r) => r.refetch())),
  }
}

export function useLandingPreview() {
  const results = useQueries({
    queries: [
      {
        queryKey: ['metrics', 'summary'],
        queryFn: api.getMetricsSummary,
      },
      {
        queryKey: ['pulls'],
        queryFn: api.getPulls,
      },
    ],
  })

  const [metrics, pulls] = results
  const topPull = pulls.data?.[0]

  return {
    portfolioSummary: metrics.data,
    topPull,
    isLoading: results.some((r) => r.isLoading),
    isError: results.some((r) => r.isError),
  }
}
