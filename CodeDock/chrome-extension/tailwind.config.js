/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        editor: {
          bg: '#1e1e2e',
          surface: '#2a2a3c',
          border: '#3a3a4c',
          text: '#cdd6f4',
          muted: '#6c7086',
        },
        accent: {
          blue: '#89b4fa',
          cyan: '#94e2d5',
          green: '#a6e3a1',
          red: '#f38ba8',
          yellow: '#f9e2af',
        },
      },
    },
  },
  plugins: [],
};