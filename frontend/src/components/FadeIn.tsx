import type { ReactNode } from 'react'
import { useInView } from '../hooks/useInView'

interface FadeInProps {
  children: ReactNode
  className?: string
  delay?: number
  direction?: 'up' | 'down' | 'none'
  once?: boolean
}

const directionClass = {
  up: 'animate-fade-up',
  down: 'animate-fade-down',
  none: 'animate-fade-in',
}

export default function FadeIn({
  children,
  className = '',
  delay = 0,
  direction = 'up',
  once = true,
}: FadeInProps) {
  const { ref, inView } = useInView<HTMLDivElement>({ once })

  return (
    <div
      ref={ref}
      className={`${directionClass[direction]} ${inView ? 'is-visible' : ''} ${className}`}
      style={{ animationDelay: `${delay}ms` }}
    >
      {children}
    </div>
  )
}
