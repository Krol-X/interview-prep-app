<script setup>
import { computed } from 'vue'
import { store, isDone, reset, cycleTheme } from '../lib/store.js'

const props = defineProps({ sections: Array, current: String })
const emit = defineEmits(['select', 'help'])

const counted = computed(() => props.sections.map((s, idx) => {
  const its = s.items.filter(i => !store.hotOnly || i.hot)
  const done = its.filter(i => isDone(i.id)).length
  return { ...s, idx, total: its.length, done, key: idx < 9 ? String(idx + 1) : '⇧' + (idx - 8) }
}))
const total = computed(() => counted.value.reduce((a, s) => a + s.total, 0))
const done = computed(() => counted.value.reduce((a, s) => a + s.done, 0))
const pct = computed(() => total.value ? Math.round(done.value / total.value * 100) : 0)
const groups = computed(() => {
  const out = []
  for (const s of counted.value) {
    if (!out.length || out[out.length - 1].name !== s.group) out.push({ name: s.group, list: [] })
    out[out.length - 1].list.push(s)
  }
  return out
})
const short = t => t.replace(/\s*\(.*?\)\s*/g, '').trim()
</script>

<template>
  <aside>
    <div class="brand label">interview prep</div>
    <div class="total"><b>{{ pct }}%</b><span class="n">{{ done }} / {{ total }}</span></div>
    <div class="bar"><i :style="{ width: pct + '%' }"></i></div>
    <div class="tools">
      <input class="search" v-model="store.query" placeholder="поиск  /" autocomplete="off" spellcheck="false">
      <label class="toggle"><input type="checkbox" v-model="store.hotOnly"> только важное</label>
      <label class="toggle"><input type="checkbox" v-model="store.hideDone"> скрыть сделанное</label>
    </div>
    <nav>
      <template v-for="g in groups" :key="g.name">
        <div class="grp label">{{ g.name }}</div>
        <button v-for="s in g.list" :key="s.id" class="sec"
          :class="{ on: s.id === current, done: s.total && s.done === s.total }"
          @click="emit('select', s.id)">
          <span class="k">{{ s.key }}</span>
          <span class="t">{{ short(s.title) }}</span>
          <span class="n">{{ s.done }}/{{ s.total }}</span>
        </button>
      </template>
    </nav>
    <div class="foot">
      <span>{{ store.persistent ? 'сохраняется' : 'превью: не сохраняется' }}</span>
      <span style="display:flex;gap:12px;align-items:center">
        <button @click="confirm('Сбросить все отметки?') && reset()">сбросить</button>
        <button class="theme" @click="cycleTheme()" :title="'тема: ' + ({ system: 'системная', light: 'светлая', dark: 'тёмная' })[store.theme] + ' (t)'">{{ ({ system: '◐', light: '○', dark: '●' })[store.theme] }}</button>
        <button class="help" @click="emit('help')">?</button>
      </span>
    </div>
  </aside>
</template>
