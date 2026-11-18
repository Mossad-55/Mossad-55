"""Snapshot public stats into a consistently aligned dark activity panel."""
from pathlib import Path
import re
import urllib.request
from svgkit import panel, namespace_ids, TOP, PAD, INNER, tile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

def embed(url, x, y, w, h, prefix):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-builder"})
    s = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    if "Something went wrong" in s:
        raise RuntimeError("Stats service returned an error")
    s = namespace_ids(s, prefix)
    s = re.sub(r'^\s*<\?xml[^>]*>', '', s)
    # Show the final state even when a viewer suppresses animation.
    s = re.sub(r'@keyframes\s+[^{]+\{(?:[^{}]|\{[^{}]*\})*\}', '', s)
    s = s.replace('opacity: 0;', 'opacity: 1;')
    s = re.sub(r'animation:[^;}]+[;]?', '', s)
    start = s.index("<svg")
    end = s.index(">", start)
    tag = s[start:end]
    tag = re.sub(r'\s(?:width|height|x|y)="[^"]*"', '', tag)
    tag = re.sub(r'\spreserveAspectRatio="[^"]*"', '', tag)
    s = s[:start] + tag + f' x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMinYMin meet"' + s[end:]
    return s

base = "https://github-readme-stats.vercel.app/api"
style = "&hide_border=true&bg_color=151922&title_color=8A63F5&text_color=F0F3F6&icon_color=8A63F5&border_radius=14&disable_animations=true"
body = tile(PAD, TOP, 540, 195) + tile(PAD + 564, TOP, 540, 195)
body += embed(base + "?username=Mossad-55&hide=prs,issues,contribs&hide_rank=true&show_icons=true&card_width=540" + style,
             PAD + 8, TOP + 8, 524, 179, "stats-")
body += embed(base + "/top-langs/?username=Mossad-55&layout=compact&langs_count=6&card_width=540" + style,
              PAD + 572, TOP + 8, 524, 179, "langs-")
(OUT / "activity.svg").write_text(panel("GitHub Activity", "public repository statistics", TOP + 195 + PAD, body), encoding="utf-8")

game = ROOT.parent / "github-breakout" / "out" / "custom.svg"
if game.exists():
    s = game.read_text(encoding="utf-8")
    s = s.replace('<svg width="822" height="242"', f'<svg x="{PAD}" y="{TOP}" width="{INNER}" height="325"')
    s = namespace_ids(s, "game-")
    (OUT / "breakout.svg").write_text(panel("Contribution Breakout", "your contributions, in play", TOP + 325 + PAD, s), encoding="utf-8")
