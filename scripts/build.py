#!/usr/bin/env python3
"""Generate the profile SVGs (hero + project map) in light and dark.

Star counts come from the GitHub API. Set GITHUB_TOKEN to avoid rate limits;
without network access the last known counts in FALLBACK_STARS are used.
"""

import json
import os
import pathlib
import urllib.request
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {
        "bg0": "#0d1117", "bg1": "#161b22", "border": "#30363d",
        "text": "#e6edf3", "muted": "#8b949e", "grid": "#21262d",
        "green": "#3fb950", "orange": "#f7a41d", "yellow": "#ffd33d",
        "purple": "#d2a8ff", "teal": "#39c5cf", "trace": "#30363d",
        "bolt0": "#ffd33d", "bolt1": "#f7a41d",
    },
    "light": {
        "bg0": "#ffffff", "bg1": "#f6f8fa", "border": "#d0d7de",
        "text": "#1f2328", "muted": "#59636e", "grid": "#d8dee4",
        "green": "#1a7f37", "orange": "#bc6c00", "yellow": "#d4a72c",
        "purple": "#8250df", "teal": "#0a7f8a", "trace": "#d0d7de",
        "bolt0": "#ffc233", "bolt1": "#f08c00",
    },
}

REPOS = {
    "sublime_zk": "renerocksai/sublime_zk",
    "sublimeless_zk": "renerocksai/sublimeless_zk",
    "telekasten.nvim": "nvim-telekasten/telekasten.nvim",
    "omajop": "renerocksai/omajop",
    "omajot": "renerocksai/omajot",
    "zap": "zigzap/zap",
    "bounded/http": "technologylab-ai/bounded-http",
    "baz": "technologylab-ai/baz",
    "Bûllets": "renerocksai/bullets",
    "bullets-server": "renerocksai/bullets-server",
    "slides": "renerocksai/slides",
    "rayslides": "technologylab-ai/rayslides",
    "dockercr": "renerocksai/dockercr",
}

FALLBACK_STARS = {
    "sublime_zk": 505, "sublimeless_zk": 203, "telekasten.nvim": 1691,
    "omajop": 2, "omajot": 0, "zap": 3416, "bounded/http": 9, "baz": 26,
    "Bûllets": 19, "bullets-server": 1, "slides": 60, "rayslides": 8,
    "dockercr": 2,
}


def fetch_stars():
    stars = dict(FALLBACK_STARS)
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "renerocksai-profile"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for name, repo in REPOS.items():
        try:
            req = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                stars[name] = json.load(resp)["stargazers_count"]
        except Exception as err:  # keep the last known count
            print(f"warning: {repo}: {err}")
    return stars


def fmt_stars(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def text(x, y, s, size, fill, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


# ---------------------------------------------------------------- hero

def hero(t):
    W, H = 1200, 360
    cmd = './case-study --question "is it cool?"'
    char_w = 20 * 0.6
    steps = len(cmd)
    widths = ";".join(f"{i * char_w:.1f}" for i in range(steps + 1))
    cursor_x = ";".join(f"{102 + i * char_w:.1f}" for i in range(steps + 1))
    key_times = ";".join(f"{i / steps:.4f}" for i in range(steps + 1))

    # lightning bolt + circuit traces feeding it
    bolt = "1062,48 954,198 1016,198 978,314 1104,150 1040,150 1080,48"
    traces = [
        "M 954 198 L 910 198 L 890 218 L 850 218",
        "M 992 120 L 950 120 L 925 95 L 870 95",
        "M 978 290 L 940 290 L 915 315 L 860 315",
        "M 1092 160 L 1130 160 L 1150 140 L 1180 140",
        "M 1070 60 L 1100 60 L 1125 35",
        "M 1030 250 L 1090 250 L 1110 270 L 1180 270",
    ]
    pads = [(850, 218), (870, 95), (860, 315), (1180, 140), (1125, 35), (1180, 270)]

    trace_svg = []
    for i, d in enumerate(traces):
        trace_svg.append(f'<path d="{d}" stroke="{t["trace"]}" stroke-width="3" fill="none" stroke-linejoin="round"/>')
        trace_svg.append(
            f'<path class="flow" d="{d}" stroke="{t["orange"]}" stroke-width="3" fill="none" '
            f'stroke-linecap="round" stroke-dasharray="14 220" style="animation-delay:-{i * 0.7:.1f}s"/>')
    for x, y in pads:
        trace_svg.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{t["bg1"]}" stroke="{t["trace"]}" stroke-width="3"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Rene Schallner: software engineer turned AI researcher and engineer. I build things to find out if they are cool.">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg0"]}"/>
  </linearGradient>
  <linearGradient id="boltfill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{t["bolt0"]}"/><stop offset="1" stop-color="{t["bolt1"]}"/>
  </linearGradient>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.4" fill="{t["grid"]}"/>
  </pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0.15"/><stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="fademask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="14" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{t["orange"]}" stop-opacity="0.28"/><stop offset="1" stop-color="{t["orange"]}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="typed"><rect x="102" y="284" height="40" width="0">
    <animate attributeName="width" begin="0.8s" dur="2.6s" fill="freeze" calcMode="discrete" values="{widths}" keyTimes="{key_times}"/>
  </rect></clipPath>
  <style>
    .flow {{ animation: flow 3.2s linear infinite; }}
    @keyframes flow {{ from {{ stroke-dashoffset: 234; }} to {{ stroke-dashoffset: 0; }} }}
    .bolt {{ animation: flicker 6s ease-in-out infinite; }}
    @keyframes flicker {{ 0%, 100% {{ opacity: 1; }} 46% {{ opacity: 1; }} 48% {{ opacity: .55; }} 50% {{ opacity: 1; }} 52% {{ opacity: .75; }} 54% {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .flow, .bolt {{ animation: none; }} }}
  </style>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#fademask)"/>
  <circle cx="1030" cy="180" r="230" fill="url(#halo)"/>
  {"".join(trace_svg)}
  <polygon class="bolt" points="{bolt}" fill="url(#boltfill)" filter="url(#glow)"/>

  {text(64, 76, "rene@vienna", 20, t["green"], 600)}{text(64 + 11 * 12, 76, ":", 20, t["muted"])}{text(64 + 12 * 12, 76, "~/code", 20, t["purple"], 600)}{text(64 + 19 * 12, 76, "$ whoami", 20, t["muted"])}
  {text(60, 158, "Rene Schallner", 78, t["text"], 800, extra='letter-spacing="-1"')}
  {text(64, 208, "software engineer → AI researcher & engineer", 27, t["muted"])}
  {text(64, 250, "I build things to find out if they're", 28, t["text"])}{text(64 + 38 * 16.8, 250, "cool.", 28, t["orange"], 800)}

  {text(64, 312, "$", 20, t["green"], 700)}
  <g clip-path="url(#typed)">{text(102, 312, cmd, 20, t["text"])}</g>
  <rect x="102" y="294" width="11" height="23" fill="{t["orange"]}">
    <animate attributeName="x" begin="0.8s" dur="2.6s" fill="freeze" calcMode="discrete" values="{cursor_x}" keyTimes="{key_times}"/>
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>
  </rect>
  <g opacity="0">
    <animate attributeName="opacity" begin="3.8s" dur="0.4s" to="1" fill="freeze"/>
    {text(102 + (steps + 2) * char_w, 312, "→ yes, it is.", 20, t["green"], 700)}
  </g>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["border"]}"/>
</svg>
'''


# ---------------------------------------------------------------- map

def project_map(t, stars):
    W, H = 1000, 660
    lines = {
        # name: (color key, pill label, pill right edge x, y, path d)
        "nocloud": ("teal", "no cloud", 480, 100,
                    "M 480 100 L 830 100 Q 880 100 880 150 L 880 220"),
        "notes": ("green", "notes", 150, 220, "M 150 220 L 880 220"),
        "web": ("orange", "web · zig", 480, 370,
                "M 480 370 L 830 370 Q 880 370 880 320 L 880 220"),
        "slides": ("purple", "slides", 150, 500, "M 150 500 L 800 500"),
    }
    # (label, x, y, line, label position)
    stations = [
        ("dockercr", 545, 100, "nocloud", "2022", "below"),
        ("sublime_zk", 190, 220, "notes", "2017", "below"),
        ("sublimeless_zk", 350, 220, "notes", "2018", "below"),
        ("telekasten.nvim", 545, 220, "notes", "2021", "below"),
        ("omajop", 720, 220, "notes", "2026", "below"),
        ("zap", 545, 370, "web", "2023", "below"),
        ("bounded/http", 670, 370, "web", "2026", "below"),
        ("baz", 800, 370, "web", "2026", "below"),
        ("Bûllets", 200, 500, "slides", "2020", "above"),
        ("slides", 545, 500, "slides", "2021", "above"),
        ("rayslides", 800, 500, "slides", "2025", "above"),
        ("bullets-server", 380, 590, "branch", "2020", "below"),
    ]

    out = []
    # faint grid
    out.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
    out.append(text(40, 46, "// how my projects are related", 17, t["muted"]))
    out.append(text(W - 40, 46, "stars refresh daily", 15, t["muted"], anchor="end", extra='font-style="italic"'))

    # the bullets-server branch: multiplayer grew into the phone companion + Crowdplay
    branch = "M 200 500 Q 200 590 250 590 L 700 590 Q 800 590 800 500"
    out.append(f'<path d="{branch}" stroke="{t["purple"]}" stroke-width="4" fill="none" '
               f'stroke-dasharray="2 10" stroke-linecap="round" opacity="0.9"/>')
    out.append(text(560, 578, "multiplayer → phone remote + Crowdplay", 15, t["purple"], anchor="middle", extra='font-style="italic"'))

    for key, (color, label, pill_x, y, d) in lines.items():
        c = t[color]
        dash = ' stroke-dasharray="1 13"' if key == "nocloud" else ""
        width = 5 if key == "nocloud" else 8
        out.append(f'<path id="line-{key}" d="{d}" stroke="{c}" stroke-width="{width}" fill="none" stroke-linecap="round"{dash}/>')
        pw = len(label) * 9.6 + 28
        out.append(f'<rect x="{pill_x - pw - 10}" y="{y - 17}" width="{pw}" height="34" rx="17" fill="{c}"/>')
        out.append(text(pill_x - 10 - pw / 2, y + 6, label, 16, t["bg0"], 700, anchor="middle"))
        # a train running along the line
        dur = {"nocloud": 7, "notes": 11, "web": 6, "slides": 9}[key]
        out.append(f'<rect x="-11" y="-3.5" width="22" height="7" rx="3.5" fill="{t["text"]}" opacity="0.9">'
                   f'<animateMotion dur="{dur}s" repeatCount="indefinite" rotate="auto"><mpath href="#line-{key}"/></animateMotion></rect>')

    # annotations on the connectors into omajot
    out.append(text(578, 86, "ssh / tailscale, not somebody's cloud", 15, t["teal"], extra='font-style="italic"'))
    out.append(text(866, 312, "baz serves the hub", 15, t["orange"], anchor="end", extra='font-style="italic"'))

    for name, x, y, line, year, pos in stations:
        c = t["purple"] if line == "branch" else t[lines[line][0]]
        r = 7 if line == "branch" else 10
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["bg0"]}" stroke="{c}" stroke-width="4"/>')
        n = stars.get(name, 0)
        meta = f"{year} · ★ {fmt_stars(n)}" if n >= 5 else year
        name_y, meta_y = (y - 44, y - 22) if pos == "above" else (y + 36, y + 58)
        out.append(text(x, name_y, name, 19, t["text"], 700, anchor="middle"))
        out.append(text(x, meta_y, meta, 15, t["muted"], anchor="middle"))

    # omajot: where the lines meet
    ox, oy = 880, 220
    out.append(f'<circle cx="{ox}" cy="{oy}" r="18" fill="none" stroke="{t["green"]}" stroke-width="3">'
               f'<animate attributeName="r" values="18;38" dur="2.4s" repeatCount="indefinite"/>'
               f'<animate attributeName="opacity" values="0.7;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="18" fill="{t["bg0"]}" stroke="{t["text"]}" stroke-width="6"/>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="7" fill="{t["green"]}"/>')
    out.append(text(ox + 28, oy - 2, "omajot", 21, t["text"], 800))
    out.append(text(ox + 28, oy + 19, "2026", 15, t["muted"]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A metro map of Rene's projects. Notes line: sublime_zk, sublimeless_zk, telekasten.nvim, omajop, omajot. Web line: zap, bounded/http, baz, which serves the omajot hub. Slides line: Bullets, slides, rayslides, with bullets-server's multiplayer growing into rayslides' phone remote. No-cloud line: dockercr leads to omajot.">
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.2" fill="{t["grid"]}"/>
  </pattern>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{t["bg1"]}"/>
{chr(10).join(out)}
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["border"]}"/>
</svg>
'''


def main():
    stars = fetch_stars()
    ASSETS.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (ASSETS / f"hero-{name}.svg").write_text(hero(theme))
        (ASSETS / f"map-{name}.svg").write_text(project_map(theme, stars))
    print("stars:", stars)


if __name__ == "__main__":
    main()
