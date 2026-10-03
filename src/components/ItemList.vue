<script setup>
import { computed, watch, nextTick } from 'vue'
import { renderInline } from '../lib/content.js'
import { isDone } from '../lib/store.js'

const props = defineProps({ section: Object, items: Array, query: String, openId: String })
const emit = defineEmits(['open', 'toggle', 'menu'])

const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
function title(i) {
  let h = renderInline(i.title)
  if (props.query) {
    const re = new RegExp('(' + esc(props.query) + ')', 'ig')
    h = h.replace(/(^|>)([^<]+)/g, (_, a, b) => a + b.replace(re, '<mark>$1</mark>'))
  }
  return h
}

// группировка по sub
const rows = computed(() => {
  const out = []; let last = null
  for (const i of props.items) {
    if (i.sub && i.sub !== last) { out.push({ type: 'sub', text: i.sub, key: 'sub:' + i.sub }); last = i.sub }
    out.push({ type: 'item', item: i, key: i.id })
  }
  return out
})

const doneCount = computed(() => props.section?.items.filter(i => isDone(i.id)).length ?? 0)

watch(() => props.openId, async id => {
  await nextTick()
  document.querySelector(`.row[data-id="${CSS.escape(id || '')}"]`)?.scrollIntoView({ block: 'nearest' })
})
</script>

<template>
  <section>
    <div class="lhead">
      <button class="menu" @click="emit('menu')" aria-label="разделы"><i></i></button>
      <h2>{{ section?.title }}</h2>
      <span class="n">{{ doneCount }} / {{ section?.items.length }}</span>
    </div>
    <div class="rows">
      <template v-for="r in rows" :key="r.key">
        <div v-if="r.type === 'sub'" class="sub label">{{ r.text }}</div>
        <div v-else class="row" :data-id="r.item.id"
          :class="{ ok: isDone(r.item.id), hot: r.item.hot, open: r.item.id === openId }"
          @click="emit('open', r.item.id)">
          <span class="box" @click.stop="emit('toggle', r.item.id)"></span>
          <span class="txt"><i v-if="r.item.hot" class="dot"></i><span v-html="title(r.item)"></span></span>
        </div>
      </template>
      <div v-if="!rows.length" class="empty">пусто</div>
    </div>
  </section>
</template>
