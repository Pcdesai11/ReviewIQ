interface DataStatusProps {
  isLoading: boolean
  isError: boolean
  error: Error | null
  onRetry?: () => void
}

export default function DataStatus({ isLoading, isError, error, onRetry }: DataStatusProps) {
  if (isLoading) {
    return (
      <div className="mx-auto max-w-6xl px-6 py-16 sm:px-10">
        <p className="font-sans text-sm text-ink-muted animate-pulse">Loading dashboard data…</p>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="mx-auto max-w-6xl px-6 py-16 sm:px-10">
        <div className="rounded-sm border border-brick/30 bg-brick/5 px-5 py-4">
          <p className="font-sans text-sm font-medium text-brick">Could not reach the Results API</p>
          <p className="mt-1 font-sans text-xs text-ink-muted">
            {error?.message ?? 'Unknown error'} — make sure the backend is running on port 8001.
          </p>
          {onRetry && (
            <button
              type="button"
              onClick={onRetry}
              className="mt-3 font-sans text-xs text-navy underline transition-colors hover:text-brass"
            >
              Try again
            </button>
          )}
        </div>
      </div>
    )
  }

  return null
}
