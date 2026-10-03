import { reactive } from 'vue'

const KEY = 'prep-ai'
const saved = JSON.parse(localStorage.getItem(KEY) || '{}')
// пути /ai/<id>/* проксируются на upstream (render.yaml routes + vite proxy)
export const PROVIDERS = {
  gemini:   { name: 'Gemini',        base: '/ai/gemini/v1beta/openai', model: 'gemini-2.5-flash',          keys: 'aistudio.google.com/apikey' },
  groq:     { name: 'Groq',          base: '/ai/groq/openai/v1',       model: 'llama-3.3-70b-versatile',   keys: 'console.groq.com/keys' },
  cerebras: { name: 'Cerebras',      base: '/ai/cerebras/v1',          model: 'gpt-oss-120b',              keys: 'cloud.cerebras.ai' },
  mistral:  { name: 'Mistral',       base: '/ai/mistral/v1',           model: 'mistral-small-latest',      keys: 'console.mistral.ai/api-keys' },
  zen:      { name: 'OpenCode Zen',  base: '/ai/zen/v1',               model: 'deepseek-v4-flash',         keys: 'opencode.ai → Keys' },
}
export const ai = reactive({
  provider: saved.provider || 'gemini',
  keys: saved.keys || {},        // provider -> apiKey
  models: saved.models || {},    // provider -> model override
  open: false,
})
export function saveAi() { localStorage.setItem(KEY, JSON.stringify({ provider: ai.provider, keys: ai.keys, models: ai.models })) }
export const cur = () => PROVIDERS[ai.provider] || PROVIDERS.gemini
export const apiKey = () => ai.keys[ai.provider] || ''
export const model = () => ai.models[ai.provider] || cur().model

export function systemPrompt(item) {
  const plain = item.body.replace(/\s+\n/g, '\n')
  return `Ты помогаешь готовиться к собеседованию на позицию Ruby/Rails-разработчика в биткоин-компанию (Hodl Hodl).
Кандидат — веб-программист с опытом PHP/Laravel и Vue, объясняй через аналогии с веб-разработкой, по-русски, кратко и без воды.
Если просят проверить ответ на английском — исправь грамматику и предложи более естественную формулировку.
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
  const res = await fetch(`${cur().base}/chat/completions`, {
    method: 'POST', signal,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey()}` },
    body: JSON.stringify({ model: model(), messages, stream: true }),
  })
  if (!res.ok) {
    let msg = `${res.status}`
    try { msg += ' ' + (await res.json()).error?.message } catch {}
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
