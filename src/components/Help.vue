<script setup>
import { ai, PROVIDERS } from '../lib/ai.js'
defineProps({ persistent: Boolean, count: Number })
const emit = defineEmits(['close', 'export', 'import'])
</script>

<template>
  <div class="overlay" @click.self="emit('close')">
    <div class="modal" role="dialog" aria-label="Клавиши">
      <div class="mh"><span class="label">Клавиши</span><button @click="emit('close')">esc</button></div>
      <table class="keys">
        <tr><th>Навигация</th></tr>
        <tr><td><kbd>j</kbd> <kbd>↓</kbd></td><td>следующий пункт (открывает его)</td></tr>
        <tr><td><kbd>k</kbd> <kbd>↑</kbd></td><td>предыдущий пункт</td></tr>
        <tr><td><kbd>g</kbd> / <kbd>G</kbd></td><td>первый / последний пункт</td></tr>
        <tr><td><kbd>]</kbd> <kbd>[</kbd></td><td>следующий / предыдущий раздел</td></tr>
        <tr><td><kbd>1</kbd>…<kbd>9</kbd></td><td>разделы 1–9</td></tr>
        <tr><td><kbd>shift</kbd>+<kbd>1</kbd>…<kbd>4</kbd></td><td>разделы 10–13</td></tr>
        <tr><th>Действия</th></tr>
        <tr><td><kbd>space</kbd> <kbd>x</kbd> <kbd>enter</kbd></td><td>отметить / снять открытый пункт</td></tr>
        <tr><td><kbd>/</kbd></td><td>поиск (по заголовкам и тексту)</td></tr>
        <tr><td><kbd>esc</kbd></td><td>закрыть пункт / выйти из поиска / закрыть окно</td></tr>
        <tr><th>Фильтры</th></tr>
        <tr><td><kbd>h</kbd></td><td>только важное</td></tr>
        <tr><td><kbd>d</kbd></td><td>скрыть сделанное</td></tr>
        <tr><th>Прочее</th></tr>
        <tr><td><kbd>?</kbd></td><td>это окно</td></tr>
        <tr><td><kbd>r</kbd></td><td>сбросить все отметки</td></tr>
        <tr><td><kbd>e</kbd></td><td>экспорт отметок в файл</td></tr>
        <tr><td><kbd>i</kbd></td><td>импорт из файла (объединяется с текущими)</td></tr>
        <tr><td><kbd>a</kbd></td><td>спросить нейросеть по открытой карточке (<kbd>ctrl</kbd>+<kbd>enter</kbd> — отправить)</td></tr>
        <tr><td><kbd>t</kbd></td><td>светлая / тёмная тема</td></tr>
      </table>
      <div class="io">
        <span class="label">Прогресс · {{ count }} отмечено</span>
        <span class="io-btns">
          <button @click="emit('export')">↓ экспорт</button>
          <button @click="emit('import')">↑ импорт</button>
        </span>
      </div>
      <div class="aiset" @keydown.stop>
        <select v-model="ai.provider">
          <option v-for="(p, id) in PROVIDERS" :key="id" :value="id">{{ p.name }}</option>
        </select>
        <input v-model.trim="ai.models[ai.provider]" :placeholder="PROVIDERS[ai.provider].model" style="width:200px" title="модель (пусто = по умолчанию)">
        <input v-model.trim="ai.keys[ai.provider]" type="password" :placeholder="'API key · ' + PROVIDERS[ai.provider].keys" autocomplete="off" style="grid-column:1/-1">
      </div>
      <div v-if="!persistent" class="mf">В превью отметки не сохраняются (sandbox).</div>
    </div>
  </div>
</template>
