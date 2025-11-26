/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0066CC',
          hover: '#0052A3',
          active: '#003D7A',
          light: '#E6F2FF',
        },
        success: {
          DEFAULT: '#00AA44',
          hover: '#008833',
          light: '#E6F9ED',
        },
        error: {
          DEFAULT: '#CC0000',
          hover: '#AA0000',
          light: '#FFE6E6',
        },
        warning: {
          DEFAULT: '#FFAA00',
          hover: '#CC8800',
          light: '#FFF4E6',
        },
        neutral: {
          primary: '#1A1A1A',
          secondary: '#4A4A4A',
          tertiary: '#8A8A8A',
          border: '#CCCCCC',
          background: '#F5F5F5',
          white: '#FFFFFF',
        },
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['SF Mono', 'Monaco', 'Courier New', 'monospace'],
      },
      fontSize: {
        'h1': ['32px', { lineHeight: '40px', fontWeight: '700' }],
        'h2': ['24px', { lineHeight: '32px', fontWeight: '700' }],
        'h3': ['20px', { lineHeight: '28px', fontWeight: '600' }],
        'h4': ['18px', { lineHeight: '24px', fontWeight: '600' }],
        'h5': ['16px', { lineHeight: '22px', fontWeight: '600' }],
        'body-lg': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'body': ['14px', { lineHeight: '20px', fontWeight: '400' }],
        'body-sm': ['12px', { lineHeight: '16px', fontWeight: '400' }],
        'body-xs': ['11px', { lineHeight: '14px', fontWeight: '400' }],
        'caption': ['11px', { lineHeight: '16px', fontWeight: '400' }],
        'button': ['14px', { lineHeight: '20px', fontWeight: '600' }],
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '48px',
      },
      borderRadius: {
        'DEFAULT': '6px',
        'lg': '8px',
      },
      boxShadow: {
        'sm': '0 2px 4px rgba(0, 0, 0, 0.1)',
        'md': '0 4px 8px rgba(0, 0, 0, 0.12)',
        'lg': '0 8px 24px rgba(0, 0, 0, 0.15)',
        'xl': '0 12px 32px rgba(0, 0, 0, 0.18)',
      },
      transitionDuration: {
        'fast': '150ms',
        'base': '300ms',
        'slow': '500ms',
      },
    },
  },
  plugins: [],
};


