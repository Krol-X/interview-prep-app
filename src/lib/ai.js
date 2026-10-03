import { reactive } from 'vue'

const KEY = 'prep-ai'
const saved = JSON.parse(localStorage.getItem(KEY) || '{}')
export const ai = reactive({
  apiKey: saved.apiKey || '',
  model: saved.model || 'big-pickle',
  open: false,
})
export function saveAi() { localStorage.setItem(KEY, JSON.stringify({ apiKey: ai.apiKey, model: ai.model })) }

const BASE = '/zen/v1'   // проксируется на https://opencode.ai/zen/v1 (render.yaml / vite proxy)

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
  const res = await fetch(`${BASE}/chat/completions`, {
    method: 'POST', signal,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${ai.apiKey}` },
    body: JSON.stringify({ model: ai.model, messages, stream: true }),
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
