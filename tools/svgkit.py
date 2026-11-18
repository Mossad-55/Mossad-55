"""Shared design system for the profile SVG panels.

Every panel is 1200 units wide with 48 units of inner padding, so all panels
line up exactly when stacked at 100% width in the README.
"""
from html import escape
import re

W = 1200
PAD = 48
INNER = W - 2 * PAD
RADIUS = 20

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Ubuntu, Arial, sans-serif"
MONO = "'Cascadia Mono', Consolas, 'SFMono-Regular', Menlo, 'DejaVu Sans Mono', monospace"

PURPLE = "#512BD4"
LILAC = "#8A63F5"
SOFT = "#B9A5FF"
TEXT = "#F0F3F6"
MUTED = "#9DA7B3"
DIM = "#6E7681"
BG1 = "#0D1117"
BG2 = "#11151D"
TILE = "#151922"
STROKE = "#2A303B"
GREEN = "#3FB950"


def esc(s) -> str:
    return escape(str(s), quote=True)


def text_width(s: str, size: float, mono: bool = False) -> float:
    return len(s) * size * (0.6 if mono else 0.53)


def panel(title: str, subtitle: str, height: int, body: str, *, style: str = "", extra_defs: str = "",
          label: str | None = None) -> str:
    """A full-width dark panel with a title row; body is drawn in panel coordinates."""
    head = ""
    if title:
        head = f"""
  <rect x="{PAD}" y="{PAD - 2}" width="5" height="30" rx="2.5" fill="url(#accent)"/>
  <text x="{PAD + 20}" y="{PAD + 22}" font-family="{SANS}" font-size="26" font-weight="700" fill="{TEXT}">{esc(title)}</text>
  <text x="{W - PAD}" y="{PAD + 21}" font-family="{SANS}" font-size="15" fill="{DIM}" text-anchor="end">{esc(subtitle)}</text>
  <rect x="{PAD}" y="{PAD + 48}" width="{INNER}" height="1" fill="{STROKE}"/>"""
    aria = esc(label or title)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="{aria}">
  <title>{aria}</title>
  <style>{style}</style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BG1}"/><stop offset="100%" stop-color="{BG2}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{PURPLE}"/><stop offset="100%" stop-color="{LILAC}"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{LILAC}" stop-opacity="0.06"/><stop offset="100%" stop-color="{LILAC}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect width="{W}" height="{height}" rx="{RADIUS}"/></clipPath>
    {extra_defs}
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{height}" fill="url(#bg)"/>
    <circle cx="{W - 120}" cy="0" r="320" fill="url(#glow)"/>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" rx="{RADIUS}" fill="none" stroke="{STROKE}"/>{head}
  {body}
</svg>
"""


# Content starts below the title row.
TOP = PAD + 49 + 32


def tile(x: float, y: float, w: float, h: float, r: int = 14) -> str:
    return f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{r}" fill="{TILE}" stroke="{STROKE}"/>'


def chip(x: float, y: float, label: str, size: int = 13) -> tuple[str, float]:
    w = text_width(label, size, mono=True) + 24
    h = size + 13
    svg = (f'<rect x="{x + 0.5:.1f}" y="{y + 0.5}" width="{w - 1:.1f}" height="{h - 1}" rx="{h / 2}" fill="#1E1542" stroke="{LILAC}" stroke-opacity="0.35"/>'
           f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + size * 0.35:.1f}" font-family="{MONO}" font-size="{size}" fill="{SOFT}" text-anchor="middle">{esc(label)}</text>')
    return svg, w


def chips(x: float, y: float, labels: list[str], size: int = 13, gap: int = 8) -> str:
    out = []
    for label in labels:
        s, w = chip(x, y, label, size)
        out.append(s)
        x += w + gap
    return "".join(out)


def pill(x: float, y: float, label: str, color: str = SOFT, size: int = 11, anchor_end: bool = False) -> str:
    w = text_width(label, size) + 8 + len(label) * 1.1 + 22
    h = 24
    if anchor_end:
        x -= w
    return (f'<rect x="{x + 0.5:.1f}" y="{y + 0.5}" width="{w - 1:.1f}" height="{h - 1}" rx="{h / 2}" fill="none" stroke="{color}" stroke-opacity="0.45"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 16}" font-family="{SANS}" font-size="{size}" font-weight="600" letter-spacing="1.1" fill="{color}" text-anchor="middle">{esc(label)}</text>')


def namespace_ids(svg: str, prefix: str) -> str:
    """Prefix ids inside an embedded SVG so several can live in one document."""
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = re.sub(rf'\bid="{re.escape(i)}"', f'id="{prefix}{i}"', svg)
        svg = re.sub(rf'url\(#{re.escape(i)}\)', f'url(#{prefix}{i})', svg)
        svg = re.sub(rf'href="#{re.escape(i)}"', f'href="#{prefix}{i}"', svg)
    return svg


def strip_xml_header(svg: str) -> str:
    return re.sub(r'^\s*<\?xml[^>]*>\s*', '', svg)
