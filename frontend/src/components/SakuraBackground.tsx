import type { CSSProperties } from 'react'

const petals = [
  { left: '8%', size: 11, delay: 0, duration: 28, drift: 40, opacity: 0.42, tone: 'blush' },
  { left: '18%', size: 9, delay: -6, duration: 34, drift: -55, opacity: 0.36, tone: 'cream' },
  { left: '31%', size: 13, delay: -12, duration: 26, drift: 35, opacity: 0.45, tone: 'blush' },
  { left: '44%', size: 10, delay: -4, duration: 32, drift: -30, opacity: 0.38, tone: 'pale' },
  { left: '57%', size: 12, delay: -18, duration: 30, drift: 50, opacity: 0.44, tone: 'blush' },
  { left: '68%', size: 9, delay: -9, duration: 36, drift: -45, opacity: 0.34, tone: 'cream' },
  { left: '79%', size: 11, delay: -15, duration: 27, drift: 38, opacity: 0.4, tone: 'pale' },
  { left: '91%', size: 10, delay: -21, duration: 33, drift: -28, opacity: 0.37, tone: 'blush' },
  { left: '24%', size: 8, delay: -24, duration: 38, drift: 42, opacity: 0.32, tone: 'cream' },
  { left: '52%', size: 12, delay: -3, duration: 29, drift: -52, opacity: 0.39, tone: 'pale' },
  { left: '73%', size: 10, delay: -27, duration: 31, drift: 33, opacity: 0.35, tone: 'blush' },
  { left: '86%', size: 9, delay: -11, duration: 35, drift: -38, opacity: 0.3, tone: 'cream' },
] as const

const toneClass = {
  blush: 'text-[#E4B8B8]',
  cream: 'text-[#F2E4DC]',
  pale: 'text-[#EBD0D0]',
} as const

export default function SakuraBackground() {
  return (
    <div className="sakura-bg pointer-events-none fixed inset-0 -z-10 overflow-hidden" aria-hidden="true">
      {petals.map((petal) => (
        <div
          key={petal.left + petal.delay}
          className="sakura-petal absolute"
          style={
            {
              left: petal.left,
              '--petal-size': `${petal.size}px`,
              '--petal-delay': `${petal.delay}s`,
              '--petal-duration': `${petal.duration}s`,
              '--petal-drift': `${petal.drift}px`,
              '--petal-opacity': petal.opacity,
            } as CSSProperties
          }
        >
          <svg
            viewBox="0 0 24 28"
            fill="currentColor"
            className={`h-[var(--petal-size)] w-[var(--petal-size)] ${toneClass[petal.tone]}`}
          >
            <path d="M12 1.5 C7 7.5 4.5 13 12 26.5 C19.5 13 17 7.5 12 1.5 Z" />
          </svg>
        </div>
      ))}
    </div>
  )
}
