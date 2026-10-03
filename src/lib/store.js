import { reactive, watch } from 'vue'

const KEY = 'prep-v2'
const mem = {}
const ls = {
  get(k) { try { return localStorage.getItem(k) } catch { return mem[k] ?? null } },
  set(k, v) { try { localStorage.setItem(k, v) } catch { mem[k] = v } },
  ok() { try { localStorage.setItem('__t', '1'); localStorage.removeItem('__t'); return true } catch { return false } },
}

const saved = JSON.parse(ls.get(KEY) || '{}')

export const store = reactive({
  done: saved.done || {},          // id -> timestamp
  section: saved.section || null,  // текущий раздел
  item: saved.item || null,        // открытый пункт
  hotOnly: !!saved.hotOnly,
  hideDone: !!saved.hideDone,
  query: '',
  persistent: ls.ok(),
})

watch(
  () => ({ done: store.done, section: store.section, item: store.item, hotOnly: store.hotOnly, hideDone: store.hideDone }),
  v => ls.set(KEY, JSON.stringify(v)),
  { deep: true },
)

export function toggle(id) {
  if (store.done[id]) delete store.done[id]
  else store.done[id] = Date.now()
}
export function isDone(id) { return !!store.done[id] }
export function reset() { store.done = {} }
