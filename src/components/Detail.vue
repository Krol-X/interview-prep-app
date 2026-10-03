<script setup>
import { watch, ref } from 'vue'
import { renderInline } from '../lib/content.js'

const props = defineProps({ item: Object, done: Boolean, prev: Object, next: Object })
const emit = defineEmits(['toggle', 'close', 'open'])
const body = ref(null)
watch(() => props.item?.id, () => { if (body.value) body.value.scrollTop = 0 })
const host = u => { try { return new URL(u).host.replace(/^www\./, '') } catch { return '' } }
</script>

<template>
  <section>
    <template v-if="item">
      <div class="dhead">
        <button class="back" @click="emit('close')" aria-label="назад">‹</button>
        <div style="flex:1;min-width:0">
          <div class="crumb">{{ item.section.title }} <template v-if="item.sub">· {{ item.sub }}</template></div>
          <h1 v-html="renderInline(item.title)"></h1>
        </div>
        <button class="dbtn" :class="{ ok: done }" @click="emit('toggle')">
          <span class="box"></span>{{ done ? 'повторено' : 'отметить' }}
        </button>
      </div>
      <div class="dbody" ref="body">
        <article v-if="item.filled" class="md" v-html="item.html"></article>
        <div v-else class="todo">
          содержимое ещё не написано<br>
          <code>content/{{ item.id }}.md</code>
        </div>
        <div v-if="item.links.length" class="links">
          <div class="label" style="margin-bottom:6px">почитать</div>
          <a v-for="l in item.links" :key="l.u" :href="l.u" target="_blank" rel="noopener">
            {{ l.t }}<span>{{ host(l.u) }}</span>
          </a>
        </div>
        <div class="dnav">
          <button v-if="prev" @click="emit('open', prev.id)">‹ <span v-html="renderInline(prev.title)"></span></button><span v-else></span>
          <button v-if="next" class="r" @click="emit('open', next.id)"><span v-html="renderInline(next.title)"></span> ›</button>
        </div>
      </div>
    </template>
    <div v-else class="placeholder">выбери пункт слева</div>
  </section>
</template>
