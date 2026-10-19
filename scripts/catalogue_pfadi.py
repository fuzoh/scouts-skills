"""Catalogue complet de l'espace Downloads de pfadi.swiss (paginé côté serveur, ?page=N).

Écrit build/pfadi-catalogue.yaml : `entries` (page de détail, titre, description) et `files`
au format manifeste (url finale, name, size, sha256, found_on) pour `ingest --match`.
Ne télécharge (pour hacher) que les fichiers dont le nom correspond à un original local sans file_url.
"""
import hashlib, re, sys, time, yaml, httpx
from urllib.parse import urljoin
from scripts import registry as reg
from scripts.discover import file_name

BASE = "https://pfadi.swiss/fr/publications-telechargements/downloads/"
UA = {"User-Agent": "skills-scoutisme-discover/0.1"}
wanted = {}
for s in reg.all_sources():
    if s["type"] != "web" and not s.get("file_url"):
        for p in reg.original_files(s["id"]):
            wanted[p.name] = s["id"]
known = {f["found_on"]: f for f in yaml.safe_load(open("build/pfadi.yaml"))["files"] if "/downloads/detail/" in f["found_on"]}

entries, files = [], {}
with httpx.Client(headers=UA, timeout=30, follow_redirects=True) as c:
    n = 1
    while True:
        r = c.get(BASE, params={"page": n}); r.raise_for_status(); time.sleep(1)
        html = r.text
        for m in re.finditer(r'<article class="event-item download-item">(.*?)</article>', html, re.S):
            a = re.search(r'<h3><a href="([^"]+)"[^>]*>(.*?)</a></h3>\s*<p>(.*?)</p>', m.group(1), re.S)
            if not a: continue
            url = urljoin(BASE, a.group(1)).rstrip("/")
            entries.append({"url": url, "title": re.sub(r"\s+", " ", a.group(2)).strip(), "description": re.sub(r"\s+", " ", a.group(3)).strip()})
        last = re.search(r'\?page=(\d+)">dernier', html)
        print(f"page {n}/{last.group(1) if last else '?'} : {len(entries)} entrées", flush=True)
        if not last or n >= int(last.group(1)): break
        n += 1
    for e in entries:
        if e["url"] in known:
            f = known[e["url"]]; files[f["url"]] = f; e["file"] = f["url"]; continue
        try:
            h = c.head(e["url"]); final = str(h.url)
        except httpx.HTTPError as exc:
            print("!", e["url"], exc, flush=True); continue
        time.sleep(1)
        e["file"] = final
        name = file_name(final)
        entry = {"url": final, "name": name, "size": int(h.headers.get("content-length") or 0), "sha256": "", "found_on": e["url"], "id": ""}
        if name in wanted:
            dg = hashlib.sha256(); size = 0
            with c.stream("GET", final) as r:
                for ch in r.iter_bytes(): dg.update(ch); size += len(ch)
            entry.update(sha256=dg.hexdigest(), size=size); time.sleep(1)
            print("haché", name, "→", wanted[name], flush=True)
        files[final] = entry
out = {"root": BASE, "retrieved": reg.today().isoformat(), "entries": entries,
       "pages": [], "files": [f for f in files.values() if f.get("sha256")]}
yaml.safe_dump(out, open("build/pfadi-catalogue.yaml", "w"), allow_unicode=True, sort_keys=False)
print("entrées", len(entries), "fichiers hachés", len(out["files"]))
