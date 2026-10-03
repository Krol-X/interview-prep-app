# usage: python3 scripts/fill.py <batch.py>  — batch.py defines ITEMS = { "dir/file.md": (links, body) }
import sys, re, runpy, json, pathlib
batch = runpy.run_path(sys.argv[1])["ITEMS"]
root = pathlib.Path("content")
n = 0
for rel, (links, body) in batch.items():
    p = root / rel
    if not p.exists():
        print("MISSING", rel); continue
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", raw)
    fm = m.group(1) if m else ""
    fm = re.sub(r"\nlinks:[\s\S]*$", "", fm).rstrip()
    if links:
        fm += "\nlinks:\n" + "".join(f"  - {{ t: {json.dumps(t, ensure_ascii=False)}, u: {json.dumps(u)} }}\n" for t, u in links)
    p.write_text(f"---\n{fm.strip()}\n---\n{body.strip()}\n", encoding="utf-8")
    n += 1
print("filled", n)
