<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { marked } from 'marked'
import { allItems, renderInline } from '../lib/content.js'
import { ai, chat, systemPrompt, model, apiKey, cur, newConv, activeConv, deleteConv, saveConvs } from '../lib/ai.js'

const props = defineProps({ item: Object })
const emit = defineEmits(['close', 'open'])

const input = ref('')
const busy = ref(false)
const err = ref('')
const showHistory = ref(false)
const log = ref(null)
const ta = ref(null)
let ctrl = null

const conv = computed(() => activeConv())
const convItem = computed(() => conv.value ? allItems.find(i => i.id === conv.value.item) : null)
const itemTitle = id => { const it = allItems.find(i => i.id === id); return it ? renderInline(it.title) : id }

// при открытии / смене карточки — продолжаем последнюю беседу по этой карточке или начинаем новую
function ensureConv() {
  if (conv.value && conv.value.item === props.item?.id) return
  const last = ai.convs.find(c => c.item === props.item?.id)
  ai.active = last ? last.id : null
}
watch(() => props.item?.id, () => { stop(); ensureConv(); showHistory.value = false }, { immediate: true })
nextTick(() => ta.value?.focus())

function stop() { ctrl?.abort(); ctrl = null; busy.value = false }
function scroll() { nextTick(() => { if (log.value) log.value.scrollTop = log.value.scrollHeight }) }
function fresh() { ai.active = null; showHistory.value = false; err.value = ''; ta.value?.focus() }
function pick(c) {
  ai.active = c.id; showHistory.value = false
  if (c.item !== props.item?.id) emit('open', c.item)   // контекст беседы = её карточка
  scroll()
}
function remove(c) { deleteConv(c.id) }

async function send() {
  const text = input.value.trim()
  if (!text || busy.value) return
  if (!apiKey()) { err.value = `Нет API-ключа для ${cur().name} — укажи его в окне ?.`; return }
  input.value = ''; err.value = ''
  const c = conv.value || newConv(props.item)
  if (!c.title) c.title = text.slice(0, 80)
  c.msgs.push({ role: 'user', content: text })
  const reply = { role: 'assistant', content: '' }
  c.msgs.push(reply); c.at = Date.now()
  busy.value = true; ctrl = new AbortController(); scroll()
  try {
    const ctxItem = allItems.find(i => i.id === c.item) || props.item
    const history = [{ role: 'system', content: systemPrompt(ctxItem) }, ...c.msgs.slice(0, -1).filter(m => m.content)]
    await chat(history, d => { reply.content += d; scroll() }, ctrl.signal)
  } catch (e) {
    if (e.name !== 'AbortError') err.value = e.message
    if (!reply.content) c.msgs.pop()
    if (!c.msgs.length) deleteConv(c.id)
  } finally { busy.value = false; ctrl = null; saveConvs(); ta.value?.focus() }
}
function onKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  if (e.key === 'Escape') { e.target.blur(); emit('close') }
}
const md = s => marked.parse(s)

// перетаскивание левого края — ширина панели
const grip = ref(false)
function startResize(e) {
  grip.value = true; document.body.classList.add('resizing')
  const x0 = e.clientX, w0 = ai.width
  const move = ev => { ai.width = Math.min(Math.max(300, w0 + (x0 - ev.clientX)), Math.round(window.innerWidth * 0.6)) }
  const up = () => { grip.value = false; document.body.classList.remove('resizing'); window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up) }
  window.addEventListener('pointermove', move); window.addEventListener('pointerup', up)
}
const when = t => { const d = new Date(t); return d.toLocaleDateString('ru', { day: 'numeric', month: 'short' }) + ' ' + d.toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }) }
</script>

<template>
  <aside class="chat" @keydown.stop>
    <div class="cgrip" :class="{ on: grip }" @pointerdown.prevent="startResize"></div>
    <div class="ch">
      <span class="label">{{ cur().name }} · {{ model() }}</span>
      <span class="cbtns">
        <button class="cbtn" :class="{ on: showHistory }" @click="showHistory = !showHistory" title="беседы">☰ {{ ai.convs.length }}</button>
        <button class="cbtn" @click="fresh" title="новая беседа">＋</button>
        <button class="cbtn" @click="emit('close')">esc</button>
      </span>
    </div>

    <!-- история бесед -->
    <div v-if="showHistory" class="clist">
      <div v-if="!ai.convs.length" class="chint">Бесед пока нет.</div>
      <div v-for="c in ai.convs" :key="c.id" class="crow" :class="{ on: c.id === ai.active }" @click="pick(c)">
        <div class="ctitle">{{ c.title || '…' }}</div>
        <div class="csub"><span v-html="itemTitle(c.item)"></span><span class="cwhen">{{ when(c.at) }}</span></div>
        <button class="cdel" @click.stop="remove(c)" title="удалить">×</button>
      </div>
    </div>

    <!-- беседа -->
    <template v-else>
      <div class="cctx" v-if="convItem && convItem.id !== item?.id">
        беседа по карточке: <b v-html="renderInline(convItem.title)"></b>
      </div>
      <div class="clog" ref="log">
        <div v-if="!conv || !conv.msgs.length" class="chint">
          Контекст — открытая карточка «<span v-html="renderInline(item.title)"></span>». Спроси что угодно по ней.
        </div>
        <template v-else>
          <div v-for="(m, i) in conv.msgs" :key="i" class="cmsg" :class="m.role">
            <div v-if="m.role === 'user'" class="ctext">{{ m.content }}</div>
            <div v-else class="md ctext" v-html="md(m.content || '…')"></div>
          </div>
        </template>
        <div v-if="err" class="cerr">{{ err }}</div>
      </div>
      <div class="cin">
        <textarea ref="ta" v-model="input" rows="2" placeholder="вопрос… (enter — отправить, shift+enter — перенос)" @keydown="onKey"></textarea>
        <button v-if="busy" class="cbtn csend stop" @click="stop" title="остановить">■</button>
        <button v-else class="cbtn csend" :disabled="!input.trim()" @click="send" title="отправить">➤</button>
      </div>
    </template>
  </aside>
</template>
