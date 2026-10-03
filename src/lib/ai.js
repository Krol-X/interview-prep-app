import { reactive, watch } from 'vue'

const KEY = 'prep-ai'
const mem = {}
const ls = {   // localStorage может быть недоступен (sandbox-iframe) — тогда держим в памяти
  get(k) { try { return localStorage.getItem(k) } catch { return mem[k] ?? null } },
  set(k, v) { try { localStorage.setItem(k, v) } catch { mem[k] = v } },
}
const saved = JSON.parse(ls.get(KEY) || '{}')
// /ai/<id>/* проксируется на upstream (render.yaml routes + vite proxy)
export const PROVIDERS = {
  gemini:   { name: 'Gemini',   base: '/ai/gemini/v1beta/openai', model: 'gemini-3.5-flash-lite',   keys: 'aistudio.google.com/apikey' },
  groq:     { name: 'Groq',     base: '/ai/groq/openai/v1',       model: 'llama-3.3-70b-versatile', keys: 'console.groq.com/keys' },
  cerebras: { name: 'Cerebras', base: '/ai/cerebras/v1',          model: 'gpt-oss-120b',            keys: 'cloud.cerebras.ai' },
  mistral:  { name: 'Mistral',  base: '/ai/mistral/v1',           model: 'ministral-14b-latest',     keys: 'console.mistral.ai/api-keys' },
}
const CKEY = 'prep-ai-convs'

export const ai = reactive({
  provider: PROVIDERS[saved.provider] ? saved.provider : 'gemini',
  keys: saved.keys || (saved.apiKey ? { gemini: saved.apiKey } : {}),       // provider -> key
  models: saved.models || (saved.model ? { gemini: saved.model } : {}),      // provider -> model override
  open: false,
  convs: JSON.parse(ls.get(CKEY) || '[]'),   // [{id, item, title, msgs:[{role,content}], at}]
  active: null,                                             // id активной беседы
})
export function saveAi() { ls.set(KEY, JSON.stringify({ provider: ai.provider, keys: ai.keys, models: ai.models })) }
watch(() => [ai.provider, ai.keys, ai.models], saveAi, { deep: true })

export function saveConvs() {
  ai.convs.sort((a, b) => b.at - a.at); ai.convs.splice(60)
  ls.set(CKEY, JSON.stringify(ai.convs))
}
export const cur = () => PROVIDERS[ai.provider]
export const apiKey = () => (ai.keys[ai.provider] || '').replace(/[^\x21-\x7e]/g, '')  // в заголовок — только печатные ASCII
export const model = () => ai.models[ai.provider] || cur().model

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
  const url = `${cur().base}/chat/completions`
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
