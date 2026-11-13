#!/usr/bin/env python3
"""Build dist/ — one standalone, hostable HTML file plus its images.

    python3 build-dist.py

Reads project/deck.json and project/slides/*.html and writes dist/index.html.
Three transforms happen on the way:

  <aside>…</aside>      lifted out into a NOTES array the N key reveals
  /_blob/<id>           rewritten to img/<file> and the file copied in
  <x-embed>…</x-embed>  turned into <iframe srcdoc> (the deck runtime is
                        not here, so the panels need a real sandbox)

Everything else is byte-for-byte the slide you authored.
"""
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(ROOT, "project", "slides")
DIST = os.path.join(ROOT, "dist")
IMG = os.path.join(DIST, "img")

# Artifact blob id -> the file on disk it was uploaded from.
BLOBS = {
    "ad3cbd868db7d7e82f788d59dee1ffb0": "demo/img/siliguri_cloud.webp",
    "fc800c7c45f8bd5d9bc5df08c788bbd4": "demo/img/siliguri_sky.webp",
    "ba85ff40eaef88d05565b4b307671ae3": "demo/img/olympus_flyover.webp",
    "094d828923a33d7baefc37fd9f759071": "demo/img/earth_day.webp",
    "818cb2efc012c2c3b0dd79b23be3dae8": "demo/img/moon_tonight.png",
}

EMBED_HEAD = (
    '<!doctype html><meta charset="utf-8">'
    "<style>html,body{margin:0;padding:0;background:transparent}</style>"
)

SHELL_HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;background:#000;overflow:hidden;font-family:'IBM Plex Sans',system-ui,sans-serif}
#stage{position:fixed;inset:0;overflow:hidden}
#deck{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:0 0}
#deck>section{position:absolute!important;left:0!important;top:0!important;
  width:1920px!important;height:1080px!important}
#bar{position:fixed;left:0;right:0;bottom:0;height:4px;background:#1a2440}
#bar>i{display:block;height:100%;background:#5AC8E8;transition:width .2s}
#n{position:fixed;right:14px;bottom:14px;font:500 15px ui-monospace,monospace;color:#44506f}
#notes{position:fixed;inset:auto 0 0 0;max-height:42vh;overflow:auto;background:#0b1020f2;
  color:#cfd6e8;padding:26px 34px;font-size:17px;line-height:1.6;white-space:pre-wrap;display:none;
  border-top:1px solid #2A3A66}
#notes.on{display:block}
#help{position:fixed;left:14px;bottom:12px;font:500 13px ui-monospace,monospace;color:#2f3950}
</style></head><body>
<div id="stage"><div id="deck">
"""

SHELL_TAIL = """</div></div>
<div id="bar"><i></i></div>
<div id="n"></div>
<div id="help">&larr; &rarr; move &middot; N notes &middot; F fullscreen</div>
<div id="notes"></div>
<script>
const NOTES=__NOTES__;
const S=[...document.querySelectorAll('#deck>section')];
S.forEach(s=>s.style.setProperty('display','none','important'));
let i=0;
function fit(){const d=document.getElementById('deck');
  const k=Math.min(innerWidth/1920,innerHeight/1080);
  d.style.transform='translate('+(-960*k)+'px,'+(-540*k)+'px) scale('+k+')';}
function show(k){
  i=Math.max(0,Math.min(S.length-1,k));
  S.forEach((s,j)=>{s.style.setProperty('display', j===i?'flex':'none','important');});
  document.querySelector('#bar>i').style.width=((i+1)/S.length*100)+'%';
  document.getElementById('n').textContent=(i+1)+' / '+S.length;
  document.getElementById('notes').textContent=NOTES[i]||'(no notes)';
  location.hash='#'+(i+1);
}
addEventListener('resize',fit);
addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown')show(i+1);
  else if(e.key==='ArrowLeft'||e.key==='PageUp')show(i-1);
  else if(e.key==='Home')show(0);
  else if(e.key==='End')show(S.length-1);
  else if(e.key.toLowerCase()==='n')document.getElementById('notes').classList.toggle('on');
  else if(e.key.toLowerCase()==='f'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();}
});
addEventListener('click',e=>{if(!e.target.closest('#notes'))show(i+1);});
fit(); show(parseInt(location.hash.slice(1))-1||0);
</script></body></html>
"""


def embeds_to_iframes(markup):
    """<x-embed style="…">inner</x-embed>  ->  <iframe … srcdoc="inner">"""

    def one(m):
        style = m.group(1) or ""
        inner = m.group(2)
        doc = EMBED_HEAD + inner
        return (
            f'<iframe style="{style};border:0;background:transparent" '
            f'scrolling="no" srcdoc="{html.escape(doc, quote=True)}"></iframe>'
        )

    return re.sub(
        r'<x-embed(?:\s+style="([^"]*)")?\s*>([\s\S]*?)</x-embed>', one, markup
    )


def build():
    deck = json.load(open(os.path.join(ROOT, "project", "deck.json")))
    order = deck["order"]
    starts = {s["start"]: s["description"] for s in deck.get("sections", {}).values()}

    os.makedirs(IMG, exist_ok=True)
    used_images = set()

    parts, notes = [], []
    for sid in order:
        path = os.path.join(SLIDES, f"{sid}.html")
        markup = open(path, encoding="utf-8").read()

        # 1. notes
        aside = re.search(r"<aside>([\s\S]*?)</aside>", markup)
        notes.append(html.unescape(aside.group(1)).strip() if aside else "")
        markup = re.sub(r"<aside>[\s\S]*?</aside>\s*", "", markup)

        # 2. images
        for bid, src in BLOBS.items():
            token = f"/_blob/{bid}"
            if token in markup:
                name = os.path.basename(src)
                markup = markup.replace(token, f"img/{name}")
                used_images.add((src, name))

        # 3. animated panels
        markup = embeds_to_iframes(markup)

        # 4. section marker, for anyone reading the HTML
        if sid in starts:
            markup = markup.replace(
                "<section ", f'<section data-section="{html.escape(starts[sid])}" ', 1
            )

        parts.append(markup.strip())

    for src, name in sorted(used_images):
        shutil.copy2(os.path.join(ROOT, src), os.path.join(IMG, name))

    # drop images no slide references any more
    for stale in set(os.listdir(IMG)) - {n for _, n in used_images}:
        os.remove(os.path.join(IMG, stale))

    out = (
        SHELL_HEAD.replace("__TITLE__", html.escape(deck["title"]))
        + "\n\n".join(parts)
        + "\n"
        + SHELL_TAIL.replace("__NOTES__", json.dumps(notes))
    )
    open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(out)

    size = os.path.getsize(os.path.join(DIST, "index.html"))
    img_bytes = sum(
        os.path.getsize(os.path.join(IMG, f)) for f in os.listdir(IMG)
    )
    print(f"{len(order)} slides  ->  dist/index.html  {size:,} bytes")
    print(f"{len(used_images)} images  ->  dist/img/     {img_bytes/1e6:.1f} MB")
    missing = [i for i, n in enumerate(notes, 1) if not n]
    if missing:
        print(f"no speaker notes on slides: {missing}")


if __name__ == "__main__":
    build()
