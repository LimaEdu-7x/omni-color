#!/usr/bin/env python3
"""omni-color: um palette.json -> rampas OKLCH -> variáveis CSS (fonte única da verdade).

Comandos
  init   --brand "#3b82f6" [--out palette.json]      cria o palette.json
  build  [palette.json] [--css theme.css] [--tailwind tw.css] [--hex ramps.hex]
  check  [palette.json] [--fix]                      portão de contraste WCAG nos pares semânticos
  scan   DIR                                         lista cores hex soltas no código
  adopt  DIR [palette.json] [--apply] [--max-de 0.03] troca hex por var(--token) (simulação por padrão)
  selftest
Usa apenas a biblioteca padrão do Python 3.
"""
import argparse, json, math, os, re, shutil, sys
from pathlib import Path

STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
LIGHTNESS = dict(zip(STEPS, [0.97, 0.94, 0.88, 0.80, 0.70, 0.62, 0.54, 0.46, 0.38, 0.30, 0.22]))
CHROMA_K = dict(zip(STEPS, [0.15, 0.30, 0.55, 0.75, 0.90, 1.0, 1.0, 0.90, 0.78, 0.62, 0.45]))
BEGIN, END = "omni-color:begin", "omni-color:end"

DEFAULT_SEMANTIC = {
    "light": {
        "bg": "neutral.50", "surface": "neutral.100", "border": "neutral.200",
        "text": "neutral.900", "text-muted": "neutral.600",
        "primary": "primary.600", "primary-hover": "primary.700", "on-primary": "neutral.50",
        "accent": "accent.600", "on-accent": "neutral.50", "ring": "primary.500",
        "success": "success.700", "warning": "warning.700", "danger": "danger.700", "info": "info.700",
    },
    "dark": {
        "bg": "neutral.950", "surface": "neutral.900", "border": "neutral.800",
        "text": "neutral.50", "text-muted": "neutral.400",
        "primary": "primary.400", "primary-hover": "primary.300", "on-primary": "neutral.950",
        "accent": "accent.400", "on-accent": "neutral.950", "ring": "primary.400",
        "success": "success.400", "warning": "warning.400", "danger": "danger.400", "info": "info.400",
    },
}
# (fg, bg, min ratio) -- pairs the gate enforces
PAIRS = [("text", "bg", 4.5), ("text", "surface", 4.5), ("text-muted", "bg", 4.5),
         ("on-primary", "primary", 4.5), ("on-accent", "accent", 4.5),
         ("success", "bg", 4.5), ("warning", "bg", 4.5), ("danger", "bg", 4.5), ("info", "bg", 4.5)]
SEMANTIC_HUES = {"success": 150, "warning": 75, "danger": 25, "info": 245}  # OKLCH hues

# ---------- colour math (OKLab / OKLCH, sRGB) ----------
def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _gam(c): return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) in (3, 4): h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def rgb_to_oklab(r, g, b):
    r, g, b = _lin(r), _lin(g), _lin(b)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

def oklab_to_rgb(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)  # linear, may be out of gamut

def hex_to_oklch(h):
    L, a, b = rgb_to_oklab(*hex_to_rgb(h))
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

def oklch_to_hex(L, C, H):
    """Out-of-gamut colours lose chroma (never lightness or hue)."""
    def rgb(c):
        a, b = c * math.cos(math.radians(H)), c * math.sin(math.radians(H))
        return oklab_to_rgb(L, a, b)
    ok = lambda rgb_: all(-1e-4 <= v <= 1 + 1e-4 for v in rgb_)
    if not ok(rgb(C)):
        lo, hi = 0.0, C
        for _ in range(30):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if ok(rgb(mid)) else (lo, mid)
        C = lo
    r, g, b = (min(1, max(0, _gam(max(0, v)))) for v in rgb(C))
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))

def luminance(h):
    r, g, b = (_lin(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

def delta_e(h1, h2):
    a, b = rgb_to_oklab(*hex_to_rgb(h1)), rgb_to_oklab(*hex_to_rgb(h2))
    return math.dist(a, b)

# ---------- palette model ----------
def make_ramp(seed_hex=None, hue=None, chroma=None):
    """11-step OKLCH ramp. If a seed is given, the closest step is pinned to the seed exactly."""
    if seed_hex:
        sl, sc, sh = hex_to_oklch(seed_hex)
    else:
        sl, sc, sh = 0.6, chroma or 0.12, hue or 0
    base_c = sc if chroma is None else chroma
    ramp = {s: oklch_to_hex(LIGHTNESS[s], base_c * CHROMA_K[s], sh) for s in STEPS}
    if seed_hex:
        ramp[min(STEPS, key=lambda s: abs(LIGHTNESS[s] - sl))] = seed_hex.lower()
    return ramp

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def resolve(pal):
    """-> ramps {name:{step:hex}}, semantic {mode:{token:hex}}"""
    seeds = pal["seeds"]
    ramps = {}
    p = seeds["primary"]
    _, pc, ph = hex_to_oklch(p)
    ramps["primary"] = make_ramp(p)
    ramps["accent"] = make_ramp(seeds["accent"]) if seeds.get("accent") else make_ramp(hue=(ph + 180) % 360, chroma=max(pc, 0.1))
    ramps["neutral"] = make_ramp(hue=ph, chroma=0.012)  # neutrals tinted toward brand
    for n, h in SEMANTIC_HUES.items():
        ramps[n] = make_ramp(seeds[n]) if seeds.get(n) else make_ramp(hue=h, chroma=0.15)
    for k, v in pal.get("overrides", {}).items():  # "primary.500": "#hex"
        name, step = k.split(".")
        ramps[name][int(step)] = v.lower()
    sem = {}
    for mode, toks in pal["semantic"].items():
        sem[mode] = {t: ramps[r.split(".")[0]][int(r.split(".")[1])] for t, r in toks.items()}
    return ramps, sem

# ---------- outputs ----------
def region(text, body, lang="css"):
    open_, close = (f"/* {BEGIN} generated: edit palette.json, not this block */", f"/* {END} */")
    block = f"{open_}\n{body}\n{close}"
    pat = re.compile(re.escape(f"/* {BEGIN}") + r".*?" + re.escape(close), re.S)
    return pat.sub(lambda _: block, text) if pat.search(text) else (text + ("\n" if text else "") + block + "\n")

def css_body(ramps, sem, pal):
    prim = [f"  --{n}-{s}: {h};" for n, r in ramps.items() for s, h in r.items()]
    def sem_lines(mode):
        return [f"  --{t}: var(--{pal['semantic'][mode][t].replace('.', '-')});" for t in sem[mode]]
    light = "\n".join(sem_lines("light"))
    dark = "\n".join(sem_lines("dark"))
    return (":root {\n" + "\n".join(prim) + "\n" + light + "\n  color-scheme: light dark;\n}\n"
            "@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {\n" + dark.replace("  --", "    --") + "\n  }\n}\n"
            ":root[data-theme=\"dark\"] {\n" + dark + "\n}")

def write_region(path, body):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(region(p.read_text(encoding="utf-8") if p.exists() else "", body), encoding="utf-8")

def cmd_init(a):
    pal = {"version": 1, "seeds": {"primary": a.brand.lower(), "accent": None, "success": None,
           "warning": None, "danger": None, "info": None}, "overrides": {}, "semantic": DEFAULT_SEMANTIC}
    if Path(a.out).exists():
        sys.exit(f"{a.out} já existe; não vou sobrescrever")
    Path(a.out).write_text(json.dumps(pal, indent=2), encoding="utf-8")
    print(f"gravado {a.out}")

def cmd_build(a):
    pal = load(a.palette)
    ramps, sem = resolve(pal)
    write_region(a.css, css_body(ramps, sem, pal))
    print(f"gravado {a.css}")
    if a.tailwind:
        body = "@theme {\n" + "\n".join(f"  --color-{n}-{s}: {h};" for n, r in ramps.items() for s, h in r.items()) + "\n}"
        write_region(a.tailwind, body)
        print(f"gravado {a.tailwind}")
    if a.hex:  # for pixel-art tools (one hex per line, no '#')
        Path(a.hex).write_text("\n".join(h[1:] for r in ramps.values() for h in r.values()) + "\n")
        print(f"gravado {a.hex}")

def fix_ref(pal, mode, fg, bg_hex, ratio):
    """Lightness-only fix: walk the fg ramp to the first step that passes."""
    ramps, _ = resolve(pal)
    name = pal["semantic"][mode][fg].split(".")[0]
    cands = sorted(STEPS, key=lambda s: -contrast(ramps[name][s], bg_hex))
    for s in cands:
        if contrast(ramps[name][s], bg_hex) >= ratio:
            return f"{name}.{s}"
    return None

def cmd_check(a):
    pal = load(a.palette)
    _, sem = resolve(pal)
    bad = 0
    for mode in sem:
        for fg, bg, need in PAIRS:
            if fg in sem[mode] and bg in sem[mode]:
                r = contrast(sem[mode][fg], sem[mode][bg])
                ok = r >= need
                print(f"{'PASS' if ok else 'FAIL'} {mode:5} {fg:11} on {bg:8} {r:5.2f} (need {need})")
                if not ok:
                    bad += 1
                    if a.fix:
                        new = fix_ref(pal, mode, fg, sem[mode][bg], need)
                        if new:
                            print(f"     fix: {fg} {pal['semantic'][mode][fg]} -> {new}")
                            pal["semantic"][mode][fg] = new
    if a.fix and bad:
        Path(a.palette).write_text(json.dumps(pal, indent=2), encoding="utf-8")
        print("palette.json atualizado (só luminosidade; matiz/croma intactos); rode build de novo")
    sys.exit(1 if bad and not a.fix else 0)

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
EXTS = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".svelte", ".vue", ".jsx", ".tsx", ".js", ".ts", ".astro"}
SKIP = {"node_modules", ".git", "dist", "build", ".next", ".omni-color-backup"}

def files(root):
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if x not in SKIP]
        for f in fs:
            if Path(f).suffix in EXTS: yield Path(d) / f

def norm(h):
    h = h.lower()
    if len(h) == 4: h = "#" + "".join(c * 2 for c in h[1:])
    return h[:7]

def token_table(pal):
    ramps, sem = resolve(pal)
    # priority groups: neutral/brand ramps first, then status ramps. Role tokens (--text, --ring…)
    # are NOT auto-assigned: which role a hex plays is a human decision.
    groups = []
    for names in (("neutral", "primary", "accent"), ("success", "warning", "danger", "info")):
        groups.append({f"{n}-{s}": h for n in names for s, h in ramps[n].items()})
    return groups

GEN_RE = re.compile(r"(/\* " + BEGIN + r".*?/\* " + END + r" \*/)", re.S)

def outside_generated(txt):
    """Text with generated regions blanked out (they are never scanned or rewritten)."""
    return GEN_RE.sub("", txt)

def cmd_scan(a):
    counts = {}
    for f in files(a.dir):
        for m in HEX_RE.findall(outside_generated(f.read_text(encoding="utf-8", errors="ignore"))):
            counts[norm(m)] = counts.get(norm(m), 0) + 1
    for h, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"{n:5}  {h}")
    print(f"{len(counts)} cores literais distintas")

def cmd_adopt(a):
    table = token_table(load(a.palette))
    changed = 0
    for f in files(a.dir):
        txt = f.read_text(encoding="utf-8", errors="ignore")
        def sub(m):
            h = norm(m.group(0))
            if len(m.group(0)) > 7: return m.group(0)  # keep alpha hex untouched
            for g in table:
                name, d = min(((n, delta_e(h, v)) for n, v in g.items()), key=lambda x: x[1])
                if d <= a.max_de: return f"var(--{name})"
            return m.group(0)
        # even indexes are user text, odd indexes are generated regions (left untouched)
        parts = GEN_RE.split(txt)
        new = "".join(HEX_RE.sub(sub, p) if i % 2 == 0 else p for i, p in enumerate(parts))
        if new != txt:
            changed += 1
            print(("reescrito " if a.apply else "reescreveria ") + str(f))
            if a.apply:
                bk = Path(a.dir) / ".omni-color-backup" / f.relative_to(a.dir)
                bk.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, bk)
                f.write_text(new, encoding="utf-8")
    print(f"{changed} arquivo(s) {'alterado(s) (backups em .omni-color-backup/)' if a.apply else 'seria(m) alterado(s); use --apply'}")

def selftest():
    assert oklch_to_hex(*hex_to_oklch("#3b82f6")) in ("#3b82f6", "#3b82f7", "#3a82f6", "#3b81f6")
    assert abs(contrast("#000000", "#ffffff") - 21) < 0.01
    assert all(re.fullmatch(r"#[0-9a-f]{6}", oklch_to_hex(0.7, 0.4, h)) for h in range(0, 360, 30))
    pal = {"seeds": {"primary": "#3b82f6"}, "overrides": {}, "semantic": DEFAULT_SEMANTIC}
    for k in ("accent", "success", "warning", "danger", "info"): pal["seeds"][k] = None
    ramps, sem = resolve(pal)
    assert len(ramps["primary"]) == 11
    assert "#3b82f6" in ramps["primary"].values()
    print("selftest ok")

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    i = s.add_parser("init"); i.add_argument("--brand", required=True); i.add_argument("--out", default="palette.json")
    b = s.add_parser("build"); b.add_argument("palette", nargs="?", default="palette.json")
    b.add_argument("--css", default="theme.css"); b.add_argument("--tailwind"); b.add_argument("--hex")
    c = s.add_parser("check"); c.add_argument("palette", nargs="?", default="palette.json"); c.add_argument("--fix", action="store_true")
    sc = s.add_parser("scan"); sc.add_argument("dir")
    ad = s.add_parser("adopt"); ad.add_argument("dir"); ad.add_argument("palette", nargs="?", default="palette.json")
    ad.add_argument("--apply", action="store_true"); ad.add_argument("--max-de", type=float, default=0.03)
    s.add_parser("selftest")
    a = p.parse_args()
    {"init": cmd_init, "build": cmd_build, "check": cmd_check, "scan": cmd_scan, "adopt": cmd_adopt,
     "selftest": lambda _: selftest()}[a.cmd](a)

if __name__ == "__main__":
    main()
