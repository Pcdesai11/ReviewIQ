import type { ReactNode } from 'react'

export type Tone = 'low' | 'mid' | 'high' | 'neutral'

const toneText: Record<Tone, string> = {
  low: 'text-forest',
  mid: 'text-brass',
  high: 'text-brick',
  neutral: 'text-ink',
}

const tonePill: Record<Tone, string> = {
  low: 'bg-forest/10 text-forest',
  mid: 'bg-brass/15 text-brass',
  high: 'bg-brick/10 text-brick',
  neutral: 'bg-navy/10 text-navy',
}

export interface ReviewRow {
  id: string
  primary: string
  secondary: string
  tagLabel?: string
  tagTone?: Tone
  value: string
  valueLabel: string
  valueTone: Tone
}

interface ReviewSectionProps {
  id: string
  eyebrow: string
  description: string
  rows: ReviewRow[]
  emptyState: string
  action?: ReactNode
}

export default function ReviewSection({
  id,
  eyebrow,
  description,
  rows,
  emptyState,
  action,
}: ReviewSectionProps) {
  return (
    <section id={id} className="py-10">
      <div className="flex items-start justify-between gap-4 border-b border-hairline pb-3">
        <div>
          <h2 className="font-sans text-xs uppercase tracking-[0.2em] text-ink-muted">
            {eyebrow}
          </h2>
          <p className="mt-1 font-display text-lg text-ink">{description}</p>
        </div>
        {action}
      </div>

      {rows.length === 0 ? (
        <p className="py-8 font-sans text-sm text-ink-muted">{emptyState}</p>
      ) : (
        <ul>
          {rows.map((row, index) => (
            <li
              key={row.id}
              className="group animate-ink-settle flex items-center justify-between gap-6 border-b border-hairline/70 py-4 transition-all duration-300 hover:bg-cream hover:pl-1"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  {row.tagLabel && row.tagTone && (
                    <span
                      className={`rounded-sm px-1.5 py-0.5 font-sans text-[11px] uppercase tracking-wide ${tonePill[row.tagTone]}`}
                    >
                      {row.tagLabel}
                    </span>
                  )}
                  <p className="truncate font-sans text-sm font-medium text-ink">{row.primary}</p>
                </div>
                <p className="mt-1 truncate font-sans text-xs text-ink-muted">{row.secondary}</p>
              </div>

              <div className="flex shrink-0 flex-col items-end">
                <span className={`font-mono tabular text-base ${toneText[row.valueTone]}`}>
                  {row.value}
                </span>
                <span className="font-sans text-[11px] uppercase tracking-wide text-ink-muted">
                  {row.valueLabel}
                </span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
