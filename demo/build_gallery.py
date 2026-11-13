"""Collect real NASA photographs of planets — no illustrations.

The NASA image library mixes spacecraft photographs with artist's impressions,
and the difference matters enormously when the picture is your evidence. This
filters on the title and description, downloads the originals, and writes a
manifest you can check.

    python demo/build_gallery.py

Keyless. Writes demo/images/ and demo/gallery.json.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request

OUT = os.path.dirname(os.path.abspath(__file__))
IMGS = os.path.join(OUT, "images")

# Words that mean "someone drew this".
NOT_A_PHOTO = re.compile(
    r"\b(illustration|artist|artwork|concept|rendering|rendition|simulat|"
    r"animation|infographic|poster|diagram|logo)\b", re.I)

# Pinned by NASA id, not by search.
#
# Searching and taking the first non-illustration hit gave: Saturn as a strip
# of rings, Mars as an annotated crater, and Pluto as an unresolved dot from
# 2006. All three are genuine photographs and none of them is the picture
# anyone means. "Not a drawing" is not the same as "the right image", so the
# heroes are chosen by hand and the filter stays as a safety net.
TARGETS = [
    ("HR 8799", "PIA17010",      "Four exoplanets, photographed"),
    ("Jupiter", "PIA21376",      "Crescent, with the Great Red Spot"),
    ("Saturn",  "PIA00400",      "Natural colour, with four icy moons"),
    ("Mars",    "PIA01249",      "Hubble's sharpest view"),
    ("Neptune", "PIA01492",      "Voyager 2, 1989 — our only visit"),
    ("Uranus",  "PIA18182",      "Voyager 2, the single flyby"),
    ("Pluto",   "PIA19857",      "True colour, 2015"),
    ("Earth",   "as11-36-5337",  "Apollo 11"),
]


def get(url, timeout=60, tries=3):
    import time
    req = urllib.request.Request(url, headers={"User-Agent": "into-the-cosmos/1.0"})
    last = None
    for n in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last = exc
            if n < tries - 1:
                time.sleep(1.5 * (n + 1))
    raise last


def search(query):
    url = ("https://images-api.nasa.gov/search?"
           + urllib.parse.urlencode({"q": query, "media_type": "image"}))
    return json.loads(get(url))["collection"]["items"]


def pick(items):
    """First result that is clearly a photograph."""
    for it in items:
        d = it["data"][0]
        text = f"{d.get('title','')} {d.get('description','')}"
        if NOT_A_PHOTO.search(text):
            continue
        return d
    return None


def meta(nasa_id):
    url = ("https://images-api.nasa.gov/search?"
           + urllib.parse.urlencode({"nasa_id": nasa_id}))
    items = json.loads(get(url))["collection"]["items"]
    return items[0]["data"][0] if items else None


def asset_url(nasa_id):
    """Ask the API where the file is instead of guessing the path.

    Ids come in several shapes — PIA17010, as11-36-5337 — and the variants
    that exist differ per asset. Constructing the URL by hand 403s often
    enough that it isn't worth it.
    """
    d = json.loads(get(f"https://images-api.nasa.gov/asset/{nasa_id}"))
    hrefs = [i["href"].replace("http://", "https://")
             for i in d["collection"]["items"]]
    for suffix in ("~orig.jpg", "~large.jpg", "~medium.jpg", ".jpg"):
        for h in hrefs:
            if h.endswith(suffix):
                return h
    return None


def main():
    os.makedirs(IMGS, exist_ok=True)
    manifest, skipped = [], 0

    for name, nid, caption in TARGETS:
        print(f"{name:<10} ← {nid}", flush=True)
        try:
            d = meta(nid)
        except Exception as exc:
            print(f"  lookup failed: {type(exc).__name__}: {exc}", flush=True)
            continue
        if d is None:
            print("  no such asset", flush=True)
            continue

        blurb = f"{d.get('title','')} {d.get('description','')}"
        if NOT_A_PHOTO.search(blurb):
            print(f"  REJECTED as a drawing: {d['title'][:50]}", flush=True)
            skipped += 1
            continue

        src = asset_url(nid)
        if not src:
            print("  no downloadable variant", flush=True)
            continue
        path = os.path.join(IMGS, f"{name.replace(' ', '_')}.jpg")
        try:
            blob = get(src, timeout=120)
            if len(blob) < 2000 or blob[:2] != b"\xff\xd8":
                print(f"  {nid}: not a usable JPEG ({len(blob)} bytes)", flush=True)
                continue
            with open(path, "wb") as fh:
                fh.write(blob)
        except Exception as exc:
            print(f"  {nid}: download failed — {exc}", flush=True)
            continue

        print(f"  ✓ {nid}  {d['title'][:52]}  ({len(blob)//1024} KB)", flush=True)
        manifest.append({
            "name": name,
            "caption": caption,
            "nasa_id": nid,
            "title": d["title"],
            "date": d.get("date_created", "")[:10],
            "description": (d.get("description") or "")[:300],
            "file": os.path.relpath(path, OUT),
        })

    with open(os.path.join(OUT, "gallery.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"\n{len(manifest)} photographs, {skipped} targets rejected as drawings")
    print(f"wrote {os.path.join(OUT, 'gallery.json')}")
    return 0 if manifest else 1


if __name__ == "__main__":
    sys.exit(main())
