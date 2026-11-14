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
    "7a1c4e9b2d6f48a3b5c7e1d9f0a2b4c6": "demo/img/milky_way.webp",
    "3f8d2a7c6b1e45d9a0c3f5b7e2d4a6c8": "demo/img/gemini_answer.png",
    "ad3cbd868db7d7e82f788d59dee1ffb0": "demo/img/siliguri_cloud.webp",
    "fc800c7c45f8bd5d9bc5df08c788bbd4": "demo/img/siliguri_sky.webp",
    "ba85ff40eaef88d05565b4b307671ae3": "demo/img/olympus_flyover.webp",
    "094d828923a33d7baefc37fd9f759071": "demo/img/earth_day.webp",
    "818cb2efc012c2c3b0dd79b23be3dae8": "demo/img/moon_tonight.png",
    "b64cefccea90fe1aa23ced1532d8b7b7": "demo/img/iss_track.webp",
    "e4b9c0d7a3f24168b5d0e9c2a7f36b14": "demo/img/repo_qr.png",
}

EMBED_HEAD = (
    '<!doctype html><meta charset="utf-8">'
    "<style>html,body{margin:0;padding:0;background:transparent}</style>"
)

SHELL_HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
/* The fonts ship with the deck. A conference wifi that does not work is
   not allowed to change what the talk looks like. */
@font-face{font-family:'IBM Plex Sans';src:url('fonts/IBMPlexSans-Variable.ttf')
  format('truetype-variations');font-weight:100 700;font-display:block}
@font-face{font-family:'JetBrains Mono';src:url('fonts/JetBrainsMono-Variable.ttf')
  format('truetype-variations');font-weight:100 800;font-display:block}
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
body.clean #help,body.clean #n,body.clean #notes{display:none}

/* ---- presenter view: the second window, on the laptop ---- */
#pv{display:none}
body.presenter{background:#05080F}
body.presenter #stage,body.presenter #bar,body.presenter #n,
body.presenter #help,body.presenter #notes{display:none}
body.presenter #pv{display:grid;position:fixed;inset:0;padding:20px;gap:18px;
  grid-template-columns:1fr minmax(320px,34%);grid-template-rows:minmax(0,1fr)}
.mini{position:relative;overflow:hidden;border-radius:12px;background:#000;
  border:1px solid #1C2742}
.mini>.holder{position:absolute;width:1920px;height:1080px;transform-origin:0 0}
.mini>.holder>section{position:absolute!important;left:0!important;top:0!important;
  width:1920px!important;height:1080px!important}
#pv-notes{grid-column:1;grid-row:1;overflow-y:auto;background:#0B1020;border:1px solid #1C2742;
  border-radius:12px;padding:26px 30px;color:#E6EAF5;font-size:24px;line-height:1.6;
  white-space:pre-wrap;min-height:0}
#pv-side{grid-column:2;grid-row:1;display:flex;flex-direction:column;gap:12px;min-height:0}
#pv-now{flex:none;height:20vh;width:100%}
#pv-next{flex:none;height:20vh;width:100%;opacity:.78}
#pv-meta{flex:none;background:#0B1020;border:1px solid #1C2742;border-radius:12px;padding:18px 20px}
#pv-clock{font:700 58px/1 'JetBrains Mono',ui-monospace,monospace;color:#7CE0A8;
  letter-spacing:2px}
#pv-clock.warn{color:#FFB454}#pv-clock.over{color:#FF6B5A}
.pv-lab{font:500 15px/1 'JetBrains Mono',ui-monospace,monospace;color:#6F7A99;
  letter-spacing:3px;text-transform:uppercase;margin-bottom:9px}
#pv-count{font:700 30px/1.2 'JetBrains Mono',ui-monospace,monospace;color:#F2F4FA;margin-top:16px}
#pv-act{font-size:19px;line-height:1.4;color:#A8B2CC;margin-top:8px}
#pv-keys{flex:none;font:500 14px/1.7 ui-monospace,monospace;color:#3b4766;padding:0 4px}
</style></head><body>
<div id="stage"><div id="deck">
"""

SHELL_TAIL = """</div></div>
<div id="bar"><i></i></div>
<div id="n"></div>
<div id="help">&larr; &rarr; move &middot; P presenter view &middot; N notes &middot; F fullscreen</div>
<div id="notes"></div>
<div id="pv">
  <div id="pv-notes"></div>
  <div id="pv-side">
    <div class="mini" id="pv-now"></div>
    <div class="mini" id="pv-next"></div>
    <div id="pv-meta">
      <div class="pv-lab">elapsed</div>
      <div id="pv-clock">00:00</div>
      <div id="pv-count"></div>
      <div id="pv-act"></div>
    </div>
    <div id="pv-keys">&larr; &rarr; move, in either window<br>T restart the clock<br>
      put the other window on the projector and press F</div>
  </div>
</div>
<script>
const NOTES=__NOTES__;
const S=[...document.querySelectorAll('#deck>section')];
S.forEach(s=>s.style.setProperty('display','none','important'));
const PRESENTER=new URLSearchParams(location.search).has('presenter');
let i=0, started=0, quiet=false;

/* The two windows talk over one channel. Either can drive. */
const CH=('BroadcastChannel' in self)?new BroadcastChannel('into-the-cosmos'):null;
function send(msg){
  if(CH)CH.postMessage(msg);
  try{localStorage.setItem('itc-sync',JSON.stringify({...msg,t:Date.now()}));}catch(e){}
}
function receive(msg){
  if(!msg)return;
  if(msg.type==='go'){
    /* Any traffic at all means a presenter window is live, whichever
       window opened first, so take the counter and hints off screen. */
    if(!PRESENTER)document.body.classList.add('clean');
    quiet=true;show(msg.i);quiet=false;
  }
  else if(msg.type==='hello'&&!PRESENTER){document.body.classList.add('clean');
    send({type:'go',i:i});}
  else if(msg.type==='clock'){started=msg.started;}
}
if(CH)CH.onmessage=e=>receive(e.data);
addEventListener('storage',e=>{
  if(e.key==='itc-sync'&&e.newValue)receive(JSON.parse(e.newValue));
});

function fit(){const d=document.getElementById('deck');
  const k=Math.min(innerWidth/1920,innerHeight/1080);
  d.style.transform='translate('+(-960*k)+'px,'+(-540*k)+'px) scale('+k+')';}

/* Draw one slide, scaled down, inside a box in the presenter window. */
function mini(box,node){
  box.innerHTML='';
  const h=document.createElement('div');h.className='holder';
  if(node){const c=node.cloneNode(true);
    c.style.setProperty('display','flex','important');h.appendChild(c);}
  box.appendChild(h);
  const k=Math.min(box.clientWidth/1920,box.clientHeight/1080);
  h.style.transform='scale('+k+')';
  h.style.left=((box.clientWidth-1920*k)/2)+'px';
  h.style.top=((box.clientHeight-1080*k)/2)+'px';
}

function act(k){for(let j=k;j>=0;j--){const a=S[j].dataset.section;if(a)return a;}return '';}

/* Shrink the note until it fits. Scrolling mid-sentence on stage is the
   one thing a presenter view must never make you do. */
function fitNotes(){
  const n=document.getElementById('pv-notes');
  let s=26;
  n.style.fontSize=s+'px';
  while(s>12&&n.scrollHeight>n.clientHeight+1){s-=1;n.style.fontSize=s+'px';}
}

function show(k){
  i=Math.max(0,Math.min(S.length-1,k));
  S.forEach((s,j)=>{s.style.setProperty('display',
    (!PRESENTER&&j===i)?'flex':'none','important');});
  document.querySelector('#bar>i').style.width=((i+1)/S.length*100)+'%';
  document.getElementById('n').textContent=(i+1)+' / '+S.length;
  document.getElementById('notes').textContent=NOTES[i]||'(no notes)';
  if(PRESENTER){
    mini(document.getElementById('pv-now'),S[i]);
    mini(document.getElementById('pv-next'),S[i+1]||null);
    document.getElementById('pv-notes').textContent=NOTES[i]||'(no notes on this one)';
    document.getElementById('pv-notes').scrollTop=0;
    fitNotes();
    document.getElementById('pv-count').textContent=(i+1)+' / '+S.length;
    document.getElementById('pv-act').textContent=act(i);
    document.title='['+(i+1)+'] presenter';
  }else{location.hash='#'+(i+1);}
  if(!quiet)send({type:'go',i:i});
}

function tick(){
  if(!PRESENTER)return;
  const s=Math.floor((Date.now()-started)/1000);
  const c=document.getElementById('pv-clock');
  c.textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+
                String(s%60).padStart(2,'0');
  c.className=s>55*60?'over':(s>45*60?'warn':'');
}

function openPresenter(){
  const u=new URL(location.href);u.searchParams.set('presenter','1');
  window.open(u.toString(),'itc-presenter','width=1400,height=900');
  document.body.classList.add('clean');
}

addEventListener('resize',()=>{fit();if(PRESENTER)show(i);});
addEventListener('keydown',e=>{
  const k=e.key.toLowerCase();
  if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();show(i+1);}
  else if(e.key==='ArrowLeft'||e.key==='PageUp')show(i-1);
  else if(e.key==='Home')show(0);
  else if(e.key==='End')show(S.length-1);
  else if(k==='p'&&!PRESENTER)openPresenter();
  else if(k==='t'){started=Date.now();send({type:'clock',started:started});tick();}
  else if(k==='n'&&!PRESENTER)document.getElementById('notes').classList.toggle('on');
  else if(k==='f'){document.fullscreenElement?document.exitFullscreen()
    :document.documentElement.requestFullscreen();}
});
addEventListener('click',e=>{if(!PRESENTER&&!e.target.closest('#notes'))show(i+1);});

if(PRESENTER){document.body.classList.add('presenter');started=Date.now();
  setInterval(tick,1000);send({type:'hello'});}
fit(); show(parseInt(location.hash.slice(1))-1||0); tick();
/* The first fit runs before the webfonts land, so size the note again
   once the real metrics are in. */
if(PRESENTER){requestAnimationFrame(()=>show(i));
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>show(i));}
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

    # the two typefaces, so the deck owes the network nothing
    fonts_out = os.path.join(DIST, "fonts")
    os.makedirs(fonts_out, exist_ok=True)
    for f in ("IBMPlexSans-Variable.ttf", "JetBrainsMono-Variable.ttf"):
        src = os.path.join(ROOT, "fonts", f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(fonts_out, f))
        else:
            print(f"!! missing font: {src}")

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
