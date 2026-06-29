import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { TrendPoint } from '../api/types'

interface TrendChartsProps {
  points: TrendPoint[]
}

function formatDate(iso: string) {
  const d = new Date(iso + 'T00:00:00')
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}

export default function TrendCharts({ points }: TrendChartsProps) {
  const data = points.map((p) => ({
    ...p,
    label: formatDate(p.date),
  }))

  return (
    <section className="py-10" id="trends">
      <p className="font-sans text-xs uppercase tracking-[0.2em] text-ink-muted">Trends</p>
      <h2 className="mt-2 font-display text-2xl text-ink">30-day signal drift</h2>
      <p className="mt-1 max-w-xl font-sans text-sm text-ink-muted">
        Risk scores, flake flags, and triage volume over the last month.
      </p>

      <div className="mt-8 grid gap-8 lg:grid-cols-2">
        <div className="rounded-sm border border-hairline bg-cream/60 p-4">
          <p className="mb-4 font-sans text-xs uppercase tracking-wider text-ink-muted">
            Average PR risk
          </p>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data}>
              <CartesianGrid stroke="#D8D0BC" strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="label" tick={{ fontSize: 10, fill: '#6B6557' }} interval="preserveStartEnd" />
              <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: '#6B6557' }} width={32} />
              <Tooltip
                contentStyle={{
                  background: '#FBF8F0',
                  border: '1px solid #D8D0BC',
                  fontFamily: 'Inter, sans-serif',
                  fontSize: 12,
                }}
              />
              <Line type="monotone" dataKey="averageRisk" stroke="#A9812F" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-sm border border-hairline bg-cream/60 p-4">
          <p className="mb-4 font-sans text-xs uppercase tracking-wider text-ink-muted">
            Flake flags &amp; triage volume
          </p>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data}>
              <CartesianGrid stroke="#D8D0BC" strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="label" tick={{ fontSize: 10, fill: '#6B6557' }} interval="preserveStartEnd" />
              <YAxis tick={{ fontSize: 10, fill: '#6B6557' }} width={32} allowDecimals={false} />
              <Tooltip
                contentStyle={{
                  background: '#FBF8F0',
                  border: '1px solid #D8D0BC',
                  fontFamily: 'Inter, sans-serif',
                  fontSize: 12,
                }}
              />
              <Line type="monotone" dataKey="flakyFlags" stroke="#2F4A3D" strokeWidth={2} dot={false} name="Flake flags" />
              <Line type="monotone" dataKey="triageCount" stroke="#1C2B3A" strokeWidth={2} dot={false} name="Triaged" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  )
}
