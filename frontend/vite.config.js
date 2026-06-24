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
    `<link rel="preload" as="style" href="${href}" crossorigin>\n    ` +
    `<script src="/load-app-css.js"></script>`
  )
}

/** Inline critical CSS and load the full bundle without blocking first paint. */
function deferAppCss() {
  return {
    name: 'defer-app-css',
    transformIndexHtml: {
      order: 'post',
      handler(html) {
        const cssHref = html.match(/\/assets\/index-[^"]+\.css/)?.[0]
        let out = html

        if (cssHref) {
          out = out
            .replace(/<script src="\/load-app-css\.js"><\/script>\s*/g, '')
            .replace(
              new RegExp(
                `<link rel="preload" as="style" href="${cssHref}" crossorigin[^>]*>`,
                'g'
              ),
              ''
            )
            .replace(
              new RegExp(`<link rel="stylesheet"[^>]*href="${cssHref}"[^>]*>`, 'g'),
              ''
            )
            .replace(
              new RegExp(
                `<noscript><link rel="stylesheet" href="${cssHref}" crossorigin></noscript>`,
                'g'
              ),
              ''
            )

          const asyncTag = asyncStylesheetTag(cssHref)
          out = out.includes('<script type="module"')
            ? out.replace('<script type="module"', `${asyncTag}\n    <script type="module"`)
            : out.replace('</head>', `${asyncTag}\n  </head>`)
        }

        return out.replace(
          '<meta charset="UTF-8" />',
          `<meta charset="UTF-8" />\n    <style id="critical-css">${criticalCss}</style>`
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
