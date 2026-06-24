import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { readFileSync } from 'node:fs'
import { fileURLToPath, URL } from 'node:url'

const criticalCss = readFileSync(
  fileURLToPath(new URL('./src/assets/styles/critical.css', import.meta.url)),
  'utf8'
)
  .replace(/\/\*[\s\S]*?\*\//g, '')
  .replace(/\s+/g, ' ')
  .trim()

function asyncStylesheetTag(href) {
  return (
    `<link rel="preload" as="style" href="${href}" crossorigin>` +
    `<link rel="stylesheet" href="${href}" media="print" onload="this.media='all';this.onload=null" crossorigin>` +
    `<noscript><link rel="stylesheet" href="${href}" crossorigin></noscript>`
  )
}

/** Inline critical CSS and load the full bundle without blocking first paint. */
function deferAppCss() {
  return {
    name: 'defer-app-css',
    transformIndexHtml: {
      order: 'post',
      handler(html) {
        const withoutBlockingCss = html
          .replace(
            /<link rel="preload" as="style" href="(\/assets\/[^"]+\.css)" crossorigin><link rel="stylesheet" crossorigin href="\1">/,
            (_, href) => asyncStylesheetTag(href)
          )
          .replace(
            /<link rel="stylesheet" crossorigin href="(\/assets\/[^"]+\.css)">/,
            (_, href) => asyncStylesheetTag(href)
          )

        return withoutBlockingCss.replace(
          '</head>',
          `<style id="critical-css">${criticalCss}</style></head>`
        )
      },
    },
  }
}

export default defineConfig({
  plugins: [vue(), deferAppCss()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
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
    allowedHosts: [
      'localhost',
      'nexxus-tech.com',
      'www.nexxus-tech.com',
    ],
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true
      },
      '/licensing/activation': {
        target: 'http://licensing:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/licensing/, '')
      }
    }
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          primevue: ['primevue']
        }
      }
    }
  }
})
