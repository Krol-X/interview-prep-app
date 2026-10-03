<script setup>
import { ref, watch, nextTick } from 'vue'
import { marked } from 'marked'
import { ai, chat, systemPrompt, cur, apiKey, model } from '../lib/ai.js'

const props = defineProps({ item: Object })
const emit = defineEmits(['close'])

const msgs = ref([])          // {role, content}
const input = ref('')
const busy = ref(false)
const err = ref('')
const log = ref(null)
const ta = ref(null)
let ctrl = null

watch(() => props.item?.id, () => { msgs.value = []; err.value = ''; stop() })
nextTick(() => ta.value?.focus())

const quick = [
  ['проще', 'Объясни суть этой карточки проще, через аналогию с веб-разработкой, в 5–7 предложениях.'],
  ['спроси меня', 'Ты интервьюер. Задай мне один вопрос по этой карточке, какой реально могут задать на собеседовании. Жди моего ответа, потом оцени его и задай следующий.'],
  ['ловушки', 'Какие уточняющие вопросы-ловушки интервьюер может задать по этой теме и как на них коротко отвечать?'],
  ['по-английски', 'Сформулируй краткий ответ по этой карточке на английском (3–5 предложений), как я бы сказал на собеседовании. Простая лексика уровня B1.'],
]

function stop() { ctrl?.abort(); ctrl = null; busy.value = false }
function scroll() { nextTick(() => { if (log.value) log.value.scrollTop = log.value.scrollHeight }) }

async function send(text) {
  text = (text ?? input.value).trim()
  if (!text || busy.value) return
  if (!apiKey()) { err.value = `Нет API-ключа для ${cur().name} — укажи его в окне ?.`; return }
  input.value = ''; err.value = ''
  msgs.value.push({ role: 'user', content: text })
  const reply = { role: 'assistant', content: '' }
  msgs.value.push(reply)
  busy.value = true; ctrl = new AbortController(); scroll()
  try {
    const history = [{ role: 'system', content: systemPrompt(props.item) }, ...msgs.value.slice(0, -1)]
    await chat(history, d => { reply.content += d; scroll() }, ctrl.signal)
  } catch (e) {
    if (e.name !== 'AbortError') err.value = e.message
    if (!reply.content) msgs.value.pop()
  } finally { busy.value = false; ctrl = null; ta.value?.focus() }
}
function onKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  if (e.key === 'Escape') { e.target.blur(); emit('close') }
}
const md = s => marked.parse(s)
</script>

<template>
  <aside class="chat" @keydown.stop>
    <div class="ch">
      <span class="label">спросить · {{ cur().name }} · {{ model() }}</span>
      <span>
        <button v-if="msgs.length" class="cbtn" @click="msgs = []">очистить</button>
        <button class="cbtn" @click="emit('close')">esc</button>
      </span>
    </div>
    <div class="cquick">
      <button v-for="[t, p] in quick" :key="t" class="cbtn" :disabled="busy" @click="send(p)">{{ t }}</button>
    </div>
    <div class="clog" ref="log">
      <div v-if="!msgs.length" class="chint">Контекст — открытая карточка. Спроси что угодно по ней или нажми кнопку выше.</div>
      <div v-for="(m, i) in msgs" :key="i" class="cmsg" :class="m.role">
        <div v-if="m.role === 'user'" class="ctext">{{ m.content }}</div>
        <div v-else class="md ctext" v-html="md(m.content || '…')"></div>
      </div>
      <div v-if="err" class="cerr">{{ err }}</div>
    </div>
    <div class="cin">
      <textarea ref="ta" v-model="input" rows="2" placeholder="вопрос… (enter — отправить, shift+enter — перенос)" @keydown="onKey"></textarea>
      <button v-if="busy" class="cbtn" @click="stop">стоп</button>
      <button v-else class="cbtn" :disabled="!input.trim()" @click="send()">↵</button>
    </div>
  </aside>
</template>
