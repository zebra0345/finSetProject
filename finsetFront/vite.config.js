import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import fs from 'fs'
import path from 'path'
// https://vite.dev/config/
export default defineConfig({
  
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'server_no_pass.key')), // 인증서 파일 경로
      cert: fs.readFileSync(path.resolve(__dirname, 'server.crt')), // 인증서 파일 경로
    },
  }
})
