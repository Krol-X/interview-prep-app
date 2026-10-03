// Загружает content/**.md во время сборки.
// Каталог = раздел (_section.md — метаданные), файл = пункт.
import { load as yamlLoad } from 'js-yaml'
import { marked } from 'marked'

const files = import.meta.glob('../../content/**/*.md', { query: '?raw', import: 'default', eager: true })

marked.setOptions({ gfm: true, breaks: false })

function parseFront(raw) {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/)
  if (!m) return [{}, raw]
  let meta = {}
  try { meta = yamlLoad(m[1]) || {} } catch (e) { console.warn('bad frontmatter', e) }
  return [meta, m[2]]
}

const sectionsMap = new Map()

for (const [path, raw] of Object.entries(files)) {
  const rel = path.replace(/^.*\/content\//, '')
  const [dir, file] = rel.split('/')
  if (!file) continue
  if (!sectionsMap.has(dir)) sectionsMap.set(dir, { id: dir, title: dir, group: '', items: [] })
  const sec = sectionsMap.get(dir)
  const [meta, body] = parseFront(raw)
  if (file === '_section.md') {
    Object.assign(sec, { title: meta.title || dir, group: meta.group || '', intro: body.trim() ? marked.parse(body) : '' })
    continue
  }
  const id = `${dir}/${file.replace(/\.md$/, '')}`
  sec.items.push({
    id,
    file,
    title: meta.title || file,
    hot: !!meta.hot,
    sub: meta.sub || null,
    links: Array.isArray(meta.links) ? meta.links : [],
    body: body.trim(),
    html: body.trim() ? marked.parse(body) : '',
    filled: body.trim().length > 0,
  })
}

export const sections = [...sectionsMap.values()]
  .sort((a, b) => a.id.localeCompare(b.id))
  .map(s => ({ ...s, items: s.items.sort((a, b) => a.file.localeCompare(b.file)) }))

export const allItems = sections.flatMap(s => s.items.map(i => ({ ...i, section: s })))

export function renderInline(md) {
  return marked.parseInline(md)
}
