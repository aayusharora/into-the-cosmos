"""The agent from the talk: "Is it worth going outside tonight?"

Four tools, all keyless, all real:

    sky_conditions   cloud cover tonight          open-meteo
    planets_tonight  what is above the horizon    JPL Horizons
    space_weather    aurora chance                NOAA SWPC
    moon_tonight     when the Moon spoils it      JPL Horizons

    python demo/tonight.py --tools-only    # no key needed
    python demo/tonight.py                 # the agent, needs GEMINI_API_KEY
"""
import json, os, sys, urllib.parse, urllib.request, datetime

SILIGURI = (26.73, 88.40)
C_TOOL, C_OK, C_DIM, C_OFF = "\033[36m", "\033[32m", "\033[90m", "\033[0m"


def _get(url, timeout=60, tries=3):
    import time
    req = urllib.request.Request(url, headers={"User-Agent": "into-the-cosmos/1.0"})
    last = None
    for n in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode()
        except Exception as exc:
            last = exc
            if n < tries - 1:
                time.sleep(1.5 * (n + 1))
    raise last


def _trace(name, **kw):
    args = ", ".join(f"{k}={v!r}" for k, v in kw.items())
    print(f"  {C_DIM}↳{C_OFF} {C_TOOL}{name}{C_OFF}({args})", flush=True)


def _horizons(body, lat, lon, start, stop):
    q = {"format": "text", "COMMAND": f"'{body}'", "OBJ_DATA": "'NO'",
         "MAKE_EPHEM": "'YES'", "EPHEM_TYPE": "'OBSERVER'",
         "CENTER": "'coord@399'", "COORD_TYPE": "'GEODETIC'",
         "SITE_COORD": f"'{lon},{lat},0'", "START_TIME": f"'{start}'",
         "STOP_TIME": f"'{stop}'", "STEP_SIZE": "'30m'",
         "QUANTITIES": "'4,9'", "ANG_FORMAT": "'DEG'", "CSV_FORMAT": "'YES'"}
    t = _get("https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(q), 90)
    rows = []
    for ln in t.split("$$SOE")[1].split("$$EOE")[0].strip().splitlines():
        p = [x.strip() for x in ln.split(",")]
        try:
            mag = None
            for q2 in p[5:]:
                try:
                    mag = float(q2); break
                except ValueError:
                    pass
            rows.append({"utc": p[0][:17], "az": float(p[3]),
                         "el": float(p[4]), "mag": mag})
        except (IndexError, ValueError):
            pass
    return rows


def _tonight_window():
    d = datetime.date.today()
    return f"{d} 12:00", f"{d + datetime.timedelta(days=1)} 00:30"


def sky_conditions(lat: float = SILIGURI[0], lon: float = SILIGURI[1]) -> dict:
    """How cloudy will it be tonight at this place, hour by hour.

    Returns the cloud cover percentage for each hour of the coming evening.
    0 is a clear sky; above about 40 there is no point going outside.
    """
    _trace("sky_conditions", lat=lat, lon=lon)
    d = json.loads(_get("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(
        {"latitude": lat, "longitude": lon, "hourly": "cloud_cover",
         "timezone": "auto", "forecast_days": 2})))
    h = d["hourly"]
    today = h["time"][0][:10]
    ev = [(t[11:16], c) for t, c in zip(h["time"], h["cloud_cover"])
          if t[:10] == today and 18 <= int(t[11:13]) <= 23]
    return {"place": [lat, lon], "evening": dict(ev),
            "average_cloud_pct": round(sum(c for _, c in ev) / max(len(ev), 1))}


def planets_tonight(lat: float = SILIGURI[0], lon: float = SILIGURI[1]) -> dict:
    """Which planets are above the horizon tonight, how high and how bright.

    Altitude is degrees above the horizon: below about 20 it is hard to see
    past buildings and haze. Magnitude is brightness. Lower is brighter, and
    anything below about 4 is visible to the naked eye.
    """
    _trace("planets_tonight", lat=lat, lon=lon)
    start, stop = _tonight_window()
    out = []
    for code, name in (("299", "Venus"), ("499", "Mars"),
                       ("599", "Jupiter"), ("699", "Saturn")):
        rows = [r for r in _horizons(code, lat, lon, start, stop) if r["el"] > 10]
        if not rows:
            continue
        best = max(rows, key=lambda r: r["el"])
        hh, mm = divmod((int(best["utc"][-5:-3]) * 60 + int(best["utc"][-2:]) + 330) % 1440, 60)
        out.append({"planet": name, "highest_altitude_deg": round(best["el"], 1),
                    "at_local_time": f"{hh:02d}:{mm:02d}", "magnitude": best["mag"]})
    return {"visible": out} if out else {"visible": [], "note": "nothing up tonight"}


def _ist(utc: str, offset_min: int = 0) -> str:
    """A Horizons UTC stamp as local Siliguri time, plus an optional offset."""
    mins = int(utc[-5:-3]) * 60 + int(utc[-2:]) + 330 + offset_min
    hh, mm = divmod(round(mins) % 1440, 60)
    return f"{hh:02d}:{mm:02d}"


def _crossing(a: dict, b: dict) -> str:
    """Local time the horizon is crossed between two samples, interpolated.

    Horizons is sampled every 30 minutes, so without this a Moon that sets
    at 19:40 is reported as 19:30 or 20:00.
    """
    span = b["el"] - a["el"]
    frac = 0.0 if span == 0 else -a["el"] / span
    return _ist(a["utc"], round(30 * frac))


def moon_tonight(lat: float = SILIGURI[0], lon: float = SILIGURI[1]) -> dict:
    """When the Moon gets out of the way, and how bright it is.

    A bright Moon above the horizon washes out everything faint. What
    matters is the dark window: if the Moon sets early or rises late, the
    rest of the night is the good part.
    """
    _trace("moon_tonight", lat=lat, lon=lon)
    start, stop = _tonight_window()
    rows = _horizons("301", lat, lon, start, stop)
    if not rows:
        return {"error": "no ephemeris for the Moon", "can_continue": True}

    if not any(r["el"] > 0 for r in rows):
        return {"above_horizon_tonight": False, "magnitude": rows[0]["mag"],
                "dark_all_night": True,
                "note": "the Moon stays down all night, so the sky is as dark as it gets"}

    # Walk the night and find where it actually crosses the horizon. The
    # first sample above the horizon is NOT a moonrise if the Moon was
    # already up when the window opened.
    rise = set_ = None
    for a, b in zip(rows, rows[1:]):
        if a["el"] <= 0 < b["el"] and rise is None:
            rise = _crossing(a, b)
        elif a["el"] > 0 >= b["el"] and set_ is None:
            set_ = _crossing(a, b)

    out = {"above_horizon_tonight": True, "magnitude": rows[0]["mag"]}
    if rows[0]["el"] > 0 and set_:
        out["already_up_at_dusk"] = True
        out["sets_local"] = set_
        out["dark_from_local"] = set_
        out["note"] = f"the Moon is already up at dusk but sets at {set_}, and the rest of the night is dark"
    elif rise:
        out["rises_local"] = rise
        out["dark_until_local"] = rise
        out["note"] = f"the sky is dark until the Moon comes up at {rise}"
    else:
        out["up_all_night"] = True
        out["note"] = "the Moon is up all night, so anything faint is washed out"
    return out


def space_weather() -> dict:
    """Current geomagnetic activity, for whether an aurora is possible.

    Kp runs 0 to 9. Below about 5 there is no aurora outside the far north.
    """
    _trace("space_weather")
    d = json.loads(_get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"))
    last = d[-1]                      # list of dicts, newest last
    kp = float(last["Kp"])
    return {"kp_index": kp, "measured_utc": last["time_tag"],
            "aurora_possible_at_mid_latitudes": kp >= 5}


# ------------------------------------------------------------------- memory
#
# previous_interaction_id carries the CONVERSATION. It does not carry the
# facts that outlive it: where you live, what you own, what you have
# already seen. Those need somewhere to sit between nights.

STORE = os.path.expanduser("~/.config/tonight/memory.json")


def _load():
    try:
        return json.load(open(STORE))
    except Exception:
        return {}


def remember(key: str, value: str) -> dict:
    """Store something worth knowing next time.

    Use it for facts that outlive the conversation: where the user is,
    what equipment they own, what they have already seen.
    """
    _trace("remember", key=key, value=value)
    d = _load()
    d[key] = value
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    json.dump(d, open(STORE, "w"), indent=1)
    return {"stored": {key: value}}


def recall() -> dict:
    """Everything known about this user from previous nights.

    Call this FIRST, before asking the user anything. If it already holds
    their location, do not ask for it again.
    """
    _trace("recall")
    d = _load()
    return d if d else {"known": "nothing yet, this is the first night"}


DATA_TOOLS = [sky_conditions, planets_tonight, moon_tonight, space_weather]
MEMORY_TOOLS = [recall, remember]
TOOLS = MEMORY_TOOLS + DATA_TOOLS
IMPL = {f.__name__: f for f in TOOLS}
QUESTION = "Is it worth stargazing tonight in Siliguri, India?"

# What the check calls each tool with. The four data tools default to
# Siliguri and need nothing. remember() needs a key and a value, and
# calling it bare is what used to make the check fail itself.
PROBE = {"remember": {"key": "_selftest", "value": "written by --tools-only"}}


def _restore(snapshot, had_store):
    """Leave the memory store exactly as the check found it."""
    if had_store:
        os.makedirs(os.path.dirname(STORE), exist_ok=True)
        json.dump(snapshot, open(STORE, "w"), indent=1)
    elif os.path.exists(STORE):
        os.remove(STORE)


def _probe(fn):
    """Run one tool. Returns True if it came back without raising."""
    try:
        out = fn(**PROBE.get(fn.__name__, {}))
        print(f"  {C_OK}✓{C_OFF} {json.dumps(out)[:200]}\n")
        return True
    except Exception as exc:
        print(f"  \033[31m✗ {fn.__name__}: {type(exc).__name__}: {exc}{C_OFF}\n")
        return False


def tools_only():
    """Call every tool with no model and no API key.

    The cheapest check there is, and the one that caught a broken tool
    while this talk was being written. Counts the four data tools, which
    are the ones that depend on somebody else's server and can break
    overnight. Memory is local, so it is checked but reported apart.
    """
    had_store, snapshot = os.path.exists(STORE), _load()

    live = sum(_probe(fn) for fn in DATA_TOOLS)
    mem = sum(_probe(fn) for fn in MEMORY_TOOLS)
    _restore(snapshot, had_store)

    print(f"{live}/{len(DATA_TOOLS)} tools working", end="")
    print("" if mem == len(MEMORY_TOOLS) else "   memory FAILED")
    return 0 if live == len(DATA_TOOLS) and mem == len(MEMORY_TOOLS) else 1


# ---------------------------------------------------------------- the agent

def _decl(fn, props=None):
    return {"type": "function", "name": fn.__name__,
            "description": (fn.__doc__ or "").strip(),
            "parameters": {"type": "object",
                           "properties": props or {}, "required": []}}


PLACE = {"lat": {"type": "number", "description": "degrees north"},
         "lon": {"type": "number", "description": "degrees east"}}
KV = {"key": {"type": "string"}, "value": {"type": "string"}}
DECLS = [_decl(recall), _decl(remember, KV),
         _decl(sky_conditions, PLACE), _decl(planets_tonight, PLACE),
         _decl(moon_tonight, PLACE), _decl(space_weather)]

SYSTEM = ("You are an observational astronomer advising a friend. Answer only "
          "from tool results, never from memory. Be specific about times and "
          "altitudes. End with a clear yes or no, and one thing to look at.")


def run_agent(model="gemini-3.5-flash"):
    if not os.environ.get("GEMINI_API_KEY"):
        kf = os.path.expanduser("~/.config/gemini/api_key")
        if os.path.exists(kf):
            os.environ["GEMINI_API_KEY"] = open(kf).read().strip()
        else:
            print("No GEMINI_API_KEY and no ~/.config/gemini/api_key"); return 2
    from google import genai
    from google.genai import types
    c = genai.Client(http_options=types.HttpOptions(timeout=90_000))
    print(f"{C_DIM}model {model} · {len(DECLS)} tools{C_OFF}\n> {QUESTION}\n", flush=True)
    log = []
    it = c.interactions.create(model=model, input=QUESTION, tools=DECLS,
                               system_instruction=SYSTEM)
    answer = ""
    for _ in range(8):
        results = []
        for st in (getattr(it, "steps", None) or []):
            if getattr(st, "type", None) != "function_call":
                continue
            args = st.arguments if isinstance(st.arguments, dict) else json.loads(st.arguments or "{}")
            try:
                out = IMPL[st.name](**args)
            except Exception as exc:
                out = {"error": f"{type(exc).__name__}: {exc}"}
            log.append({"call": st.name, "arguments": args, "result": out})
            results.append({"type": "function_result", "name": st.name,
                            "call_id": st.id,
                            "result": [{"type": "text", "text": json.dumps(out)}]})
        if (getattr(it, "output_text", "") or "").strip():
            answer = it.output_text
        if not results:
            break
        it = c.interactions.create(model=model, input=results,
                                   previous_interaction_id=it.id, tools=DECLS)
    print(f"\n{C_OK}{answer}{C_OFF}\n")
    print(f"{C_DIM}{len(log)} tool calls{C_OFF}")
    os.makedirs("demo/out", exist_ok=True)
    json.dump({"question": QUESTION, "calls": log, "answer": answer},
              open("demo/out/tonight.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(tools_only() if "--tools-only" in sys.argv else run_agent())
