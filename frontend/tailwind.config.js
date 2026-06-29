/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ivory: '#F6F2E7',
        cream: '#FBF8F0',
        ink: '#2A2722',
        'ink-muted': '#6B6557',
        navy: '#1C2B3A',
        forest: '#2F4A3D',
        brass: '#A9812F',
        brick: '#8C3F32',
        hairline: '#D8D0BC',
      },
      fontFamily: {
        display: ['Fraunces', 'serif'],
        sans: ['Inter', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      transitionTimingFunction: {
        smooth: 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
    },
  },
  plugins: [],
}
