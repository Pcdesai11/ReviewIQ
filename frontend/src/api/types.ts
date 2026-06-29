export type TriageClass = 'regression' | 'flaky' | 'infra' | 'environment'

export interface PullRequest {
  id: string
  title: string
  repo: string
  author: string
  filesChanged: number
  riskScore: number
  rationale: string
}

export interface FlakyTest {
  id: string
  name: string
  suite: string
  confidence: number
  lastFlaked: string
}

export interface TriageItem {
  id: string
  run: string
  commit: string
  classification: TriageClass
  summary: string
  minutesAgo: number
}

export interface PortfolioSummary {
  averageRisk: number
  highRiskOpenPRs: number
  flakyTestsWatched: number
  triagedToday: number
}
