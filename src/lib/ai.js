import { reactive, watch } from 'vue'

const KEY = 'prep-ai'
const mem = {}
const ls = {   // localStorage может быть недоступен (sandbox-iframe) — тогда держим в памяти
  get(k) { try { return localStorage.getItem(k) } catch { return mem[k] ?? null } },
  set(k, v) { try { localStorage.setItem(k, v) } catch { mem[k] = v } },
}
const saved = JSON.parse(ls.get(KEY) || '{}')
// /ai/gemini/* проксируется на generativelanguage.googleapis.com (render.yaml routes + vite proxy)
const BASE = '/ai/gemini/v1beta/openai'
const DEFAULT_MODEL = 'gemini-3.5-flash-lite'
const CKEY = 'prep-ai-convs'

export const ai = reactive({
  apiKey: saved.apiKey || saved.keys?.gemini || '',
  model: saved.model || saved.models?.gemini || '',
  open: false,
  convs: JSON.parse(ls.get(CKEY) || '[]'),   // [{id, item, title, msgs:[{role,content}], at}]
  active: null,                                             // id активной беседы
})
export function saveAi() { ls.set(KEY, JSON.stringify({ apiKey: ai.apiKey, model: ai.model })) }
watch(() => [ai.apiKey, ai.model], saveAi)

export function saveConvs() {
  ai.convs.sort((a, b) => b.at - a.at); ai.convs.splice(60)
  ls.set(CKEY, JSON.stringify(ai.convs))
}
export const apiKey = () => (ai.apiKey || '').replace(/[^\x21-\x7e]/g, '')  // в заголовок — только печатные ASCII
export const model = () => ai.model || DEFAULT_MODEL

export function newConv(item) {
  const c = { id: Date.now().toString(36), item: item.id, title: '', msgs: [], at: Date.now() }
  ai.convs.unshift(c); ai.active = c.id
  return c
}
export function activeConv() { return ai.convs.find(c => c.id === ai.active) || null }
export function deleteConv(id) {
  const i = ai.convs.findIndex(c => c.id === id)
  if (i >= 0) ai.convs.splice(i, 1)
  if (ai.active === id) ai.active = null
  saveConvs()
}

export function systemPrompt(item) {
  const plain = item.body.replace(/\s+\n/g, '\n')
  return `Ты помогаешь готовиться к техническому собеседованию (Ruby, Rails, PostgreSQL, Sidekiq, Bitcoin, английский для интервью).
Отвечай по-русски, кратко и по существу, без воды. Опирайся на содержимое открытой карточки; если вопрос выходит за её рамки — отвечай по теме раздела.
Если просят проверить текст на английском — исправь ошибки и предложи более естественную формулировку.
Если просят задать вопросы — задавай по одному, как интервьюер, и жди ответа.

Сейчас открыта карточка.
Раздел: ${item.section.title}
Заголовок: ${item.title}
Содержимое карточки:
---
${plain}
---`
}

// стриминг через OpenAI-совместимый chat/completions; onDelta(text) вызывается по мере прихода
export async function chat(messages, onDelta, signal) {
  const key = apiKey()
  // ключ дублируем: Authorization (прод), x-prep-key (dev-прокси превращает его в Authorization — превью режет Authorization)
  const url = `${BASE}/chat/completions`
  const res = await fetch(url, {
    method: 'POST', signal,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${key}`, 'x-prep-key': key },
    body: JSON.stringify({ model: model(), messages, stream: true }),
  })
  if (!res.ok) {
    let msg = `${res.status}`
    try {
      let j = await res.json(); if (Array.isArray(j)) j = j[0]
      msg += ' ' + (j?.error?.message || j?.message || j?.detail || JSON.stringify(j).slice(0, 200))
    } catch {}
    throw new Error(msg)
  }
  const reader = res.body.getReader(), dec = new TextDecoder()
  let buf = ''
  for (;;) {
    const { value, done } = await reader.read()
    if (done) break
    buf += dec.decode(value, { stream: true })
    const lines = buf.split('\n'); buf = lines.pop()
    for (const l of lines) {
      const s = l.trim()
      if (!s.startsWith('data:')) continue
      const data = s.slice(5).trim()
      if (data === '[DONE]') return
      try {
        const d = JSON.parse(data).choices?.[0]?.delta
        if (d?.content) onDelta(d.content)
      } catch {}
    }
  }
}
