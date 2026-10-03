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

// ── экспорт / импорт прогресса в файл ──
export function exportState() {
  const data = { app: 'prep', v: 2, exported: new Date().toISOString(), done: store.done, hotOnly: store.hotOnly, hideDone: store.hideDone }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `prep-progress-${data.exported.slice(0, 10)}.json`
  a.click()
  setTimeout(() => URL.revokeObjectURL(a.href), 1000)
}

// mode: 'merge' — объединить (сохранить и свои, и из файла), 'replace' — заменить
export function importState(mode = 'merge') {
  return new Promise(resolve => {
    const input = document.createElement('input')
    input.type = 'file'; input.accept = 'application/json,.json'
    input.onchange = async () => {
      const f = input.files?.[0]
      if (!f) return resolve(null)
      try {
        const data = JSON.parse(await f.text())
        if (data.app !== 'prep' || typeof data.done !== 'object') throw new Error('not a prep file')
        const before = Object.keys(store.done).length
        store.done = mode === 'replace' ? { ...data.done } : { ...store.done, ...data.done }
        resolve({ before, after: Object.keys(store.done).length, imported: Object.keys(data.done).length })
      } catch (e) { resolve({ error: e.message }) }
    }
    input.click()
  })
}
