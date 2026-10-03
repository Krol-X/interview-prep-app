import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// /ai/gemini/* → Google; ключ приходит в x-prep-key (превью режет Authorization) и превращается в Authorization
const proxy = {
  '/ai/gemini': {
    target: 'https://generativelanguage.googleapis.com', changeOrigin: true,
    rewrite: p => p.replace('/ai/gemini', ''),
    configure: proxy => proxy.on('proxyReq', req => {
      const k = req.getHeader('x-prep-key')
      if (k) { req.setHeader('authorization', `Bearer ${k}`); req.removeHeader('x-prep-key') }
    }),
  },
}
export default defineConfig({
  plugins: [vue()],
  server: { host: '0.0.0.0', port: 5173, allowedHosts: true, proxy },
  preview: { host: '0.0.0.0', port: 4173, allowedHosts: true, proxy },
})
