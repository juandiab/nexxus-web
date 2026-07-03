import path from 'node:path'
import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const hmrHost = env.VITE_HMR_HOST || undefined

  return {
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      host: true,
      port: 5175,
      strictPort: true,
      allowedHosts: ['v2.nexxus-tech.com', 'localhost'],
      proxy: {
        '/api': {
          target: 'http://backend:8000',
          changeOrigin: true,
        },
        '/licensing': {
          target: 'http://licensing:8001',
          changeOrigin: true,
        },
      },
      hmr: {
            host: 'v2.nexxus-tech.com',
            protocol: 'wss',
            clientPort: 443,
          },
      watch: {
        usePolling: true,
      },
    },
    clearScreen: false,
  }
})
