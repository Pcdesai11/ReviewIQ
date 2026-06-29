import type { AuditLogEntry } from '../api/types'

interface AuditTrailProps {
  entries: AuditLogEntry[]
}

function formatTime(iso: string) {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function AuditTrail({ entries }: AuditTrailProps) {
  return (
    <section className="py-10" id="audit">
      <p className="font-sans text-xs uppercase tracking-[0.2em] text-ink-muted">Audit trail</p>
      <h2 className="mt-2 font-display text-2xl text-ink">Recent model decisions</h2>
      <p className="mt-1 max-w-xl font-sans text-sm text-ink-muted">
        Every analysis logged with model, output, and action taken.
      </p>

      {entries.length === 0 ? (
        <p className="mt-6 font-sans text-sm text-ink-muted">No audit entries yet.</p>
      ) : (
        <ul className="mt-6 divide-y divide-hairline border-y border-hairline">
          {entries.map((entry) => (
            <li key={entry.id} className="py-4">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <span className="font-mono text-xs text-brass">{entry.analysisType}</span>
                <span className="font-sans text-xs text-ink-muted">{formatTime(entry.createdAt)}</span>
              </div>
              <p className="mt-1 font-sans text-sm text-ink">
                <span className="font-mono text-ink-muted">{entry.subjectId}</span>
                {' · '}
                {entry.modelProvider}/{entry.modelName}
              </p>
              <p className="mt-1 font-sans text-sm text-ink-muted line-clamp-2">{entry.output}</p>
              <p className="mt-1 font-sans text-xs text-forest">{entry.actionTaken}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
