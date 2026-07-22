import { defineConfig } from 'vite'

export default defineConfig({
  base: '/concept-book-base/',
  server: {
    proxy: {
      '/api': 'http://localhost:8200',
    },
  },
})
