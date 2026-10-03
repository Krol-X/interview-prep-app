import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export const UPSTREAMS = {
  gemini: 'https://generativelanguage.googleapis.com',
  groq: 'https://api.groq.com',
  cerebras: 'https://api.cerebras.ai',
  mistral: 'https://api.mistral.ai',
  github: 'https://models.github.ai',
  zen: 'https://opencode.ai/zen',
}
const proxy = Object.fromEntries(Object.entries(UPSTREAMS).map(([id, url]) => {
  const u = new URL(url)
  return [`/ai/${id}`, { target: u.origin, changeOrigin: true, rewrite: p => u.pathname.replace(/\/$/, '') + p.replace(`/ai/${id}`, '') }]
}))
export default defineConfig({
  plugins: [vue()],
  server: { host: '0.0.0.0', port: 5173, allowedHosts: true, proxy },
  preview: { host: '0.0.0.0', port: 4173, allowedHosts: true, proxy },
})
