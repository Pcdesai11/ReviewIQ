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

export interface TrendPoint {
  date: string
  averageRisk: number
  flakyFlags: number
  triageCount: number
}

export interface MetricsTrend {
  points: TrendPoint[]
}

export interface AuditLogEntry {
  id: string
  analysisType: string
  subjectId: string
  modelProvider: string
  modelName: string
  output: string
  actionTaken: string
  createdAt: string
}
