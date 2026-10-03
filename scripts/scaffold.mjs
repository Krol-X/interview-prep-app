// Генерирует content/<NN-section>/<slug>.md из старых чеклистов.
// Существующие файлы НЕ перезаписывает — можно запускать повторно.
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const SRC = [
  ['/home/user/interview-prep/checklist.md', 'Подготовка'],
  ['/home/user/interview-prep/english.md', 'English'],
]
const OUT = path.resolve('content')

const translit = s => s.toLowerCase()
  .replace(/[а-яё]/g, c => ({а:'a',б:'b',в:'v',г:'g',д:'d',е:'e',ё:'e',ж:'zh',з:'z',и:'i',й:'j',к:'k',л:'l',м:'m',н:'n',о:'o',п:'p',р:'r',с:'s',т:'t',у:'u',ф:'f',х:'h',ц:'c',ч:'ch',ш:'sh',щ:'sch',ъ:'',ы:'y',ь:'',э:'e',ю:'yu',я:'ya'}[c] ?? c))
  .replace(/`/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48)

const yamlStr = s => JSON.stringify(s)

let secIdx = 0
for (const [file, group] of SRC) {
  const lines = fs.readFileSync(file, 'utf8').split('\n')
  let dir = null, order = 0, sub = null, created = 0
  for (const ln of lines) {
    if (ln.startsWith('## ')) {
      secIdx++
      const title = ln.slice(3).trim()
      const slug = translit(title.replace(/\(.*?\)/g, ''))
      dir = path.join(OUT, `${String(secIdx).padStart(2, '0')}-${slug}`)
      fs.mkdirSync(dir, { recursive: true })
      const meta = path.join(dir, '_section.md')
      if (!fs.existsSync(meta)) fs.writeFileSync(meta, `---\ntitle: ${yamlStr(title)}\ngroup: ${yamlStr(group)}\n---\n`)
      order = 0; sub = null
      continue
    }
    if (!dir) continue
    if (ln.startsWith('### ')) { sub = ln.slice(4).trim(); continue }
    const m = ln.match(/^\s*- (?:\[ \] )?(.*)/)
    if (!m) continue
    let text = m[1].trim()
    const hot = text.startsWith('**') && text.endsWith('**') && text.split('**').length === 3
    if (hot) text = text.slice(2, -2)
    order++
    const base = translit(text) || crypto.createHash('md5').update(text).digest('hex').slice(0, 8)
    const fname = `${String(order).padStart(2, '0')}-${base}.md`
    const fp = path.join(dir, fname)
    if (fs.existsSync(fp)) continue
    const fm = [`title: ${yamlStr(text)}`, `hot: ${hot}`]
    if (sub) fm.push(`sub: ${yamlStr(sub)}`)
    fs.writeFileSync(fp, `---\n${fm.join('\n')}\n---\n`)
    created++
  }
  console.log(group, 'created', created)
}
