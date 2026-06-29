import type { FlakyTest, PortfolioSummary, PullRequest, TriageItem } from './types'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8001'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText)
    throw new Error(detail || `Request failed (${res.status})`)
  }
  return res.json() as Promise<T>
}

export const api = {
  getMetricsSummary: () => get<PortfolioSummary>('/v1/metrics/summary'),
  getPulls: () => get<PullRequest[]>('/v1/pulls'),
  getFlakyTests: () => get<{ tests: FlakyTest[] }>('/v1/tests/flaky').then((r) => r.tests),
  getTriageQueue: () => get<{ items: TriageItem[] }>('/v1/ci-runs/triage').then((r) => r.items),
}

export { API_BASE }
