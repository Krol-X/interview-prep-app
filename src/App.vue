<script setup>
import { computed, ref, watch, onMounted, onUnmounted } from 'vue'
import { sections, allItems, renderInline } from './lib/content.js'
import { store, toggle, isDone, reset, exportState, importState } from './lib/store.js'
import Sidebar from './components/Sidebar.vue'
import ItemList from './components/ItemList.vue'
import Detail from './components/Detail.vue'
import Help from './components/Help.vue'
import Chat from './components/Chat.vue'
import { ai } from './lib/ai.js'

const helpOpen = ref(false)
const drawerOpen = ref(false)

if (!store.section || !sections.find(s => s.id === store.section)) store.section = sections[0]?.id

const section = computed(() => sections.find(s => s.id === store.section))
const current = computed(() => allItems.find(i => i.id === store.item) || null)

const q = computed(() => store.query.trim().toLowerCase())
const matches = i => !q.value || i.title.toLowerCase().includes(q.value) || i.body.toLowerCase().includes(q.value)

const visibleItems = computed(() => {
  if (!section.value) return []
  return section.value.items.filter(i =>
    (!store.hotOnly || i.hot) && (!store.hideDone || !isDone(i.id)) && matches(i))
})

// при поиске — прыгнуть в первый раздел с совпадением
watch(q, v => {
  if (!v) return
  const curHas = section.value?.items.some(matches)
  if (curHas) return
  const hit = sections.find(s => s.items.some(matches))
  if (hit) store.section = hit.id
})

function openSection(id) { store.section = id; drawerOpen.value = false }
function openItem(id) { store.item = id; const it = allItems.find(i => i.id === id); if (it) store.section = it.section.id }
function closeItem() { store.item = null }

function step(d) {
  const list = visibleItems.value
  if (!list.length) return
  const idx = list.findIndex(i => i.id === store.item)
  const next = list[Math.min(list.length - 1, Math.max(0, idx + d))] || list[0]
  store.item = next.id
}
function stepSection(d) {
  const idx = sections.findIndex(s => s.id === store.section)
  store.section = sections[(idx + d + sections.length) % sections.length].id
  store.item = null
}

async function doImport() {
  const r = await importState('merge')
  if (!r) return
  if (r.error) alert('Не удалось импортировать: ' + r.error)
  else alert(`Импортировано ${r.imported} отметок (было ${r.before}, стало ${r.after}).`)
}
function onKey(e) {
  if (e.ctrlKey || e.metaKey || e.altKey) return
  if (helpOpen.value) { if (e.key === 'Escape' || e.key === '?') helpOpen.value = false; return }
  if (e.target.tagName === 'TEXTAREA') return
  if (e.target.tagName === 'INPUT') { if (e.key === 'Escape') { e.target.blur(); store.query = '' } return }
  const k = e.key
  if (k === 'j' || k === 'ArrowDown') { step(1); e.preventDefault() }
  else if (k === 'k' || k === 'ArrowUp') { step(-1); e.preventDefault() }
  else if (k === ' ' || k === 'x' || k === 'Enter') { if (store.item) toggle(store.item); e.preventDefault() }
  else if (k === ']') stepSection(1)
  else if (k === '[') stepSection(-1)
  else if (k === '/') { document.querySelector('.search')?.focus(); e.preventDefault() }
  else if (k === 'h') store.hotOnly = !store.hotOnly
  else if (k === 'd') store.hideDone = !store.hideDone
  else if (k === 'g') { if (visibleItems.value[0]) store.item = visibleItems.value[0].id }
  else if (k === 'G') { const l = visibleItems.value; if (l.length) store.item = l[l.length - 1].id }
  else if (k === '?') { helpOpen.value = true; e.preventDefault() }
  else if (k === 'Escape') { if (ai.open) ai.open = false; else if (drawerOpen.value) drawerOpen.value = false; else closeItem() }
  else if (k === 'r') { if (confirm('Сбросить все отметки?')) reset() }
  else if (k === 'e') exportState()
  else if (k === 'a') { if (current.value) ai.open = !ai.open }
  else if (k === 'i') doImport()
  else if (/^Digit[1-9]$/.test(e.code)) {
    const n = +e.code.slice(5) - 1 + (e.shiftKey ? 9 : 0)
    if (sections[n]) { store.section = sections[n].id; store.item = null }
    e.preventDefault()
  }
}
onMounted(() => document.addEventListener('keydown', onKey))
onUnmounted(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <div class="app">
    <div class="drawerbg" :class="{ show: drawerOpen }" @click="drawerOpen = false"></div>
    <Sidebar
      class="side" :class="{ open: drawerOpen }"
      :sections="sections" :current="store.section"
      @select="openSection" @help="helpOpen = true" />

    <ItemList
      class="list" :class="{ covered: !!current }"
      :section="section" :items="visibleItems" :query="q" :open-id="store.item"
      @open="openItem" @toggle="toggle" @menu="drawerOpen = true" />

    <Detail
      class="detail" :class="{ open: !!current }"
      :item="current" :done="current ? isDone(current.id) : false"
      :prev="visibleItems[visibleItems.findIndex(i => i.id === store.item) - 1] || null"
      :next="visibleItems[visibleItems.findIndex(i => i.id === store.item) + 1] || null"
      @toggle="toggle(current.id)" @close="closeItem" @open="openItem" @ask="ai.open = !ai.open" />

    <Chat v-if="ai.open && current" :item="current" @close="ai.open = false" />

    <Help v-if="helpOpen" @close="helpOpen = false" @export="exportState()" @import="helpOpen = false; doImport()" :persistent="store.persistent" :count="Object.keys(store.done).length" />
  </div>
</template>
