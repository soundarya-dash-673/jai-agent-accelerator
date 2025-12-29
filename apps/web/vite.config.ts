import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  // Load .env, .env.development, etc.
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [react()],
    server: {
      // port: 3000,
      proxy: {
        '/api': {
          // Use env var, fallback to localhost
          target: env.VITE_API_URL||'http://localhost:8123' ,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },
  }
})
