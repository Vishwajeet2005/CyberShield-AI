/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#080d1a',
        'bg-secondary': '#0d1528',
        'bg-card': '#111827',
        'accent-cyan': '#00d4ff',
        'accent-blue': '#0066ff',
        'danger': '#ff3366',
        'warning': '#ff9900',
        'success': '#00ff88',
        'text-primary': '#f0f4ff',
        'text-secondary': '#8899aa',
        'border-subtle': '#1e2d42',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
    },
  },
  plugins: [],
}
