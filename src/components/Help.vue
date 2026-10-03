<script setup>
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
      </table>
      <div class="io">
        <span class="label">Прогресс · {{ count }} отмечено</span>
        <span class="io-btns">
          <button @click="emit('export')">↓ экспорт</button>
          <button @click="emit('import')">↑ импорт</button>
        </span>
      </div>
      <div class="mf">
        Один пункт = один файл <code>content/&lt;раздел&gt;/&lt;пункт&gt;.md</code>. Точкой помечены важные (<code>hot: true</code>).
        <template v-if="!persistent"><br>В превью отметки не сохраняются (sandbox).</template>
      </div>
    </div>
  </div>
</template>
