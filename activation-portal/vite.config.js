import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  base: '/licensing/',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5175,
    watch: {
      usePolling: !!process.env.CHOKIDAR_USEPOLLING,
    },
    hmr: process.env.VITE_HMR_HOST
      ? {
          protocol: 'wss',
          host: process.env.VITE_HMR_HOST,
          clientPort: 443,
        }
      : true,
    allowedHosts: ['localhost', 'nexxus-tech.com', 'www.nexxus-tech.com'],
  },
})
