import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const zen = { '/zen': { target: 'https://opencode.ai', changeOrigin: true, secure: true } }
export default defineConfig({
  plugins: [vue()],
  server: { host: '0.0.0.0', port: 5173, allowedHosts: true, proxy: zen },
  preview: { host: '0.0.0.0', port: 4173, allowedHosts: true, proxy: zen },
})
