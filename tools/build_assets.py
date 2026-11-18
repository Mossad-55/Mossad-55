"""Builds the static SVG panels in ../assets."""
from pathlib import Path
import re
import urllib.request

from svgkit import (W, PAD, INNER, TOP, SANS, MONO, PURPLE, LILAC, SOFT, TEXT, MUTED, DIM, STROKE, GREEN,
                    esc, panel, tile, chips, pill, namespace_ids, strip_xml_header)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)
BODY = "#C9D1D9"


def save(name: str, svg: str) -> None:
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


# ------------------------------------------------------------------ header
def header() -> None:
    H = 362
    k, t, s, p, v, n = "#569CD6", "#4EC9B0", "#CE9178", "#D4D4D4", "#9CDCFE", "#B5CEA8"
    code = [
        [("Ahlena / backend", TEXT)],
        [("A caregiving platform in Arabic & English.", MUTED)],
        [("", MUTED)],
        [("Architecture   ", DIM), ("9-module modular monolith", SOFT)],
        [("Data           ", DIM), ("PostgreSQL · EF Core", TEXT)],
        [("Payments       ", DIM), ("Paymob checkout & refunds", TEXT)],
        [("Messaging      ", DIM), ("SignalR · outbox jobs", TEXT)],
        [("Testing        ", DIM), ("5,800+ automated tests", TEXT)],
    ]
    cw = 542
    cx, cy = W - PAD - cw, PAD
    lh = 25
    ch = 44 + len(code) * lh + 22
    rows = []
    for i, segs in enumerate(code):
        y = cy + 44 + 26 + i * lh
        spans = "".join(f'<tspan fill="{c}">{esc(txt)}</tspan>' for txt, c in segs)
        rows.append(
            f'<g class="ln" style="animation-delay:{0.25 + i * 0.15:.2f}s">'
            f'<text x="{cx + 28}" y="{y}" font-family="{MONO}" font-size="14" style="font-variant-ligatures:none" xml:space="preserve">{spans}</text></g>')
    cursor_y = cy + 44 + 26 + (len(code) - 1) * lh

    contacts = [("EMAIL", "mosad55522@gmail.com"), ("PHONE", "+20 102 141 7408"),
                ("LINKEDIN", "in/moss-ad-ahmed-28aaa6203"), ("LEETCODE", "leetcode.com/u/Mossad")]
    col = INNER / 4
    contact_svg = []
    for i, (label, value) in enumerate(contacts):
        x = PAD + i * col
        contact_svg.append(
            f'<text x="{x}" y="404" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="1.6" fill="{LILAC}">{label}</text>'
            f'<text x="{x}" y="430" font-family="{SANS}" font-size="16" fill="{TEXT}">{esc(value)}</text>')

    body = f"""
  <g class="up">
    <rect x="{PAD + 0.5}" y="{PAD + 0.5}" width="231" height="29" rx="14.5" fill="#0F2A1C" stroke="{GREEN}" stroke-opacity="0.55"/>
    <circle class="pulse" cx="{PAD + 18}" cy="{PAD + 15}" r="4.5" fill="{GREEN}"/>
    <text x="{PAD + 31}" y="{PAD + 19.5}" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="1.3" fill="#7EE787">OPEN TO WORK &amp; FREELANCE</text>
    <text x="{PAD - 3}" y="152" font-family="{SANS}" font-size="60" font-weight="700" fill="{TEXT}">Mossad Ahmed</text>
    <text x="{PAD}" y="196" font-family="{SANS}" font-size="26" font-weight="600" fill="url(#accent)">.NET Backend Developer</text>
    <text x="{PAD}" y="236" font-family="{SANS}" font-size="17" fill="{MUTED}">I work on the backend: APIs, databases, payments</text>
    <text x="{PAD}" y="261" font-family="{SANS}" font-size="17" fill="{MUTED}">and the tests that keep them working.</text>
    {chips(PAD, 292, ["ASP.NET Core", "PostgreSQL", "SignalR", "DDD", "CQRS"], 13)}
  </g>
  <rect x="{cx + 0.5}" y="{cy + 0.5}" width="{cw - 1}" height="{ch - 1}" rx="12" fill="#0D1117" stroke="#30363D"/>
  <path d="M{cx + 1} {cy + 44} V{cy + 12} a11 11 0 0 1 11 -11 H{cx + cw - 12} a11 11 0 0 1 11 11 V{cy + 44} Z" fill="#161B22"/>
  <rect x="{cx + 1}" y="{cy + 44}" width="{cw - 2}" height="1" fill="#30363D"/>
  <circle cx="{cx + 24}" cy="{cy + 22}" r="4" fill="{LILAC}"/>
  <text x="{cx + 40}" y="{cy + 27}" font-family="{MONO}" font-size="12" fill="#8B949E">PROJECT NOTES</text>
  <text x="{cx + cw - 24}" y="{cy + 27}" font-family="{MONO}" font-size="12" fill="#8B949E" text-anchor="end">Takamol · private</text>
  {''.join(rows)}
"""
    style = (".ln{animation:fade .5s ease backwards}.up{animation:rise .8s ease backwards}"
             ".cursor{animation:blink 1.1s step-end infinite}.pulse{animation:pulse 2s ease-in-out infinite}"
             "@keyframes fade{from{opacity:0}}@keyframes rise{from{opacity:0;transform:translateY(6px)}}"
             "@keyframes blink{50%{opacity:0}}@keyframes pulse{50%{opacity:.3}}")
    save("header", panel("", "", H, body, style=style, label="Mossad Ahmed - .NET Backend Developer"))
    # Separate linked images work in GitHub READMEs; links inside an SVG image do not.
    for name, label, value in [
        ("email", "EMAIL", "mosad55522@gmail.com"),
        ("phone", "PHONE", "+20 102 141 7408"),
        ("linkedin", "LINKEDIN", "Mossad Ahmed"),
        ("leetcode", "LEETCODE", "Mossad"),
    ]:
        save("contact-" + name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="288" height="82" viewBox="0 0 288 82" role="img" aria-label="{esc(label + ': ' + value)}">
<rect x="0.5" y="0.5" width="287" height="81" rx="12" fill="#151922" stroke="{STROKE}"/>
<text x="20" y="27" font-family="{SANS}" font-size="11" font-weight="700" letter-spacing="1.3" fill="{LILAC}">{label}</text>
<text x="20" y="56" font-family="{SANS}" font-size="17" fill="{TEXT}">{esc(value)}</text>
<path d="M260 24 h7 v7 M267 24 l-9 9" fill="none" stroke="{MUTED}" stroke-width="1.5"/>
</svg>""")


# ------------------------------------------------------------------ about
def about() -> None:
    lines = [
        [("I'm Mossad, a ", 0), (".NET developer", 1), (" based in Egypt. I work remotely at ", 0), ("Takamol", 1), (" and take on freelance projects", 0)],
        [("through ", 0), ("Upwork", 1), (" and ", 0), ("Mostaql", 1), (". My work includes new APIs, payment integrations and updates to older backends.", 0)],
        [("At Takamol, I built the backend for ", 0), ("Ahlena", 1), (", a platform connecting families with caregivers and care homes.", 0)],
        [("Before that, I studied Computer Science at ", 0), ("Damanhur University", 1), (" and ran problem-solving sessions with the ICPC community.", 0)],
    ]
    text = []
    for i, segs in enumerate(lines):
        spans = "".join(
            f'<tspan font-weight="700" fill="{TEXT}">{esc(s)}</tspan>' if b else esc(s) for s, b in segs)
        text.append(f'<text x="{PAD}" y="{TOP + 12 + i * 31}" font-family="{SANS}" font-size="18" fill="{BODY}" xml:space="preserve">{spans}</text>')
    metrics = [("5,800+", "automated tests on Ahlena"), ("9", "business modules designed"),
               ("2023", "CS degree · Damanhur"), ("AR / EN", "Ahlena's two languages")]
    gap = 24
    tw = (INNER - 3 * gap) / 4
    ty = TOP + 12 + 3 * 31 + 36
    th = 104
    for i, (big, small) in enumerate(metrics):
        x = PAD + i * (tw + gap)
        text.append(tile(x, ty, tw, th))
        text.append(f'<rect x="{x + 24}" y="{ty + 24}" width="22" height="3" rx="1.5" fill="url(#accent)"/>')
        text.append(f'<text x="{x + 24}" y="{ty + 64}" font-family="{SANS}" font-size="30" font-weight="700" fill="{TEXT}">{esc(big)}</text>')
        text.append(f'<text x="{x + 24}" y="{ty + 88}" font-family="{SANS}" font-size="15" fill="{MUTED}">{esc(small)}</text>')
    H = int(ty + th + PAD)
    save("about", panel("About Me", "Backend .NET Developer · Egypt", H, "".join(text)))


# ------------------------------------------------------------------ services
ICONS = {
    "api": f'<text x="-2" y="33" font-family="{MONO}" font-size="34" font-weight="700" fill="{LILAC}">{{}}</text>',
    "arch": f'<rect x="2" y="4" width="40" height="9" rx="3" fill="{LILAC}"/><rect x="2" y="18" width="40" height="9" rx="3" fill="{LILAC}" opacity=".7"/><rect x="2" y="32" width="40" height="9" rx="3" fill="{LILAC}" opacity=".45"/>',
    "rt": f'<path d="M26 1 L6 26 H20 L16 44 L38 17 H24 Z" fill="{LILAC}"/>',
    "db": f'<g fill="none" stroke="{LILAC}" stroke-width="3.5"><ellipse cx="22" cy="9" rx="17" ry="6.5"/><path d="M5 9 v26 c0 4 7.5 7 17 7 s17 -3 17 -7 v-26"/><path d="M5 22 c0 4 7.5 7 17 7 s17 -3 17 -7"/></g>',
    "fs": f'<g fill="none" stroke="{LILAC}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="40" height="34" rx="5"/><path d="M2 14 H42"/><path d="M16 22 l-5 5 l5 5 M28 22 l5 5 l-5 5"/></g>',
}


def services() -> None:
    items = [
        ("api", "Backend APIs (.NET)", ["REST APIs with auth, validation,", "pagination and OpenAPI docs."]),
        ("arch", "System Architecture", ["N-Tier, Onion or Clean Architecture,", "depending on what the project needs."]),
        ("rt", "Real-Time Systems", ["SignalR chat, live notifications,", "push and email via outbox jobs."]),
        ("db", "Database Design", ["PostgreSQL / SQL Server modeling,", "query tuning and concurrency."]),
        ("fs", "Full-Stack Apps", ["ASP.NET Core with a React frontend", "and payment integrations."]),
    ]
    gap, th = 24, 164
    tw = (INNER - 2 * gap) / 3
    parts = []
    for i, (icon, title, desc) in enumerate(items):
        x = PAD + (i % 3) * (tw + gap)
        y = TOP + (i // 3) * (th + gap)
        parts.append(tile(x, y, tw, th))
        parts.append(f'<g transform="translate({x + 28},{y + 28})">{ICONS[icon]}</g>')
        parts.append(f'<text x="{x + 88}" y="{y + 57}" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
        for j, line in enumerate(desc):
            parts.append(f'<text x="{x + 28}" y="{y + 108 + j * 25}" font-family="{SANS}" font-size="16" fill="{MUTED}">{esc(line)}</text>')
    x, y = PAD + 2 * (tw + gap), TOP + th + gap
    parts.append(f"""<clipPath id="cta"><rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14"/></clipPath>
  <rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="14" fill="url(#accent)"/>
  <circle cx="{x + tw - 30}" cy="{y + 20}" r="95" fill="#FFFFFF" opacity="0.07" clip-path="url(#cta)"/>
  <text x="{x + 28}" y="{y + 50}" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="1.6" fill="#E9E3FB">FREELANCE WORK</text>
  <text x="{x + 28}" y="{y + 92}" font-family="{SANS}" font-size="23" font-weight="700" fill="#FFFFFF">Need a .NET developer?</text>
  <text x="{x + 28}" y="{y + 133}" font-family="{SANS}" font-size="16" fill="#E9E3FB">Email me about your project.</text>""")
    H = int(TOP + 2 * th + gap + PAD)
    save("services", panel("What I Do", "for teams and freelance clients", H, "".join(parts)))


# ------------------------------------------------------------------ projects
PROJECTS = [
    ("Ahlena", "HEALTHCARE · CAREGIVING", True,
     ["Bilingual AR/EN platform connecting families,", "caregivers and care homes. 9-module modular", "monolith, Paymob payments, SignalR chat."],
     ["ASP.NET Core 10", "PostgreSQL", "CQRS", "5,800+ tests"]),
    ("TheZone", "REAL-TIME MESSAGING", False,
     ["A messaging backend using SignalR for chat,", "PostgreSQL for storage and Redis. Built with", "Clean Architecture and CQRS."],
     ["SignalR", "PostgreSQL", "Redis", "Docker"]),
    ("Bakora API", "MARKETPLACE", False,
     ["Multi-vendor services marketplace with Admin,", "Provider and Customer roles, secure online", "payments and EN/AR localization."],
     ["ASP.NET Core", "Onion Arch", "DDD", "EF Core"]),
    ("CampusPulse", "GRADUATION PROJECT", False,
     ["My graduation project: anonymous student", "feedback on professors and courses, with", "ratings from professor to university level."],
     ["Clean Arch", "JWT", "Unit of Work", "NLog"]),
    ("SchoolHub API", "EDUCATION", False,
     ["School management backend for students,", "teachers, courses, attendance and grading", "with role-based access."],
     ["ASP.NET Core", "Identity", "SQL Server", "EF Core"]),
    ("CompanyEmployees", "CQRS SHOWCASE", False,
     ["An employee management API on .NET 9.", "A focused example of separating commands", "and queries with MediatR."],
     [".NET 9", "CQRS", "MediatR", "REST"]),
]


def projects() -> None:
    gap, ch = 24, 262
    cw = (INNER - gap) / 2
    parts = []
    for i, (title, tag, private, desc, tech) in enumerate(PROJECTS):
        x = PAD + (i % 2) * (cw + gap)
        y = TOP + (i // 2) * (ch + gap)
        parts.append(tile(x, y, cw, ch))
        parts.append(f'<rect x="{x + 28}" y="{y}" width="56" height="3" rx="1.5" fill="url(#accent)"/>')
        parts.append(pill(x + 28, y + 28, tag))
        if private:
            parts.append(pill(x + cw - 28, y + 28, "PRIVATE · LIVE", GREEN, anchor_end=True))
        else:
            parts.append(pill(x + cw - 28, y + 28, "PUBLIC REPO", MUTED, anchor_end=True))
        parts.append(f'<text x="{x + 28}" y="{y + 100}" font-family="{SANS}" font-size="27" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
        for j, line in enumerate(desc):
            parts.append(f'<text x="{x + 28}" y="{y + 134 + j * 24}" font-family="{SANS}" font-size="16" fill="{MUTED}">{esc(line)}</text>')
        parts.append(chips(x + 28, y + ch - 28 - 26, tech, 13))
    H = int(TOP + 3 * ch + 2 * gap + PAD)
    save("projects", panel("Featured Projects", "github.com/Mossad-55", H, "".join(parts)))


# ------------------------------------------------------------------ tech stack
ICON_IDS = ["cs", "dotnet", "postgres", "mysql", "redis", "docker", "linux", "nginx",
            "git", "github", "postman", "react", "js", "py", "java"]


def fetch_icon(name: str) -> str:
    cache = ROOT / "tools" / ".icons"
    cache.mkdir(exist_ok=True)
    f = cache / f"{name}.svg"
    if not f.exists():
        req = urllib.request.Request(f"https://skillicons.dev/icons?i={name}&theme=dark", headers={"User-Agent": "profile-builder"})
        f.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    return f.read_text(encoding="utf-8")


def stack() -> None:
    size = 56
    step = (INNER - size) / (len(ICON_IDS) - 1)
    parts = []
    for i, name in enumerate(ICON_IDS):
        icon = namespace_ids(strip_xml_header(fetch_icon(name)), f"{name}-")
        icon = re.sub(r'<svg\b([^>]*?)\swidth="[^"]*"', r'<svg\1', icon, count=1)
        icon = re.sub(r'<svg\b([^>]*?)\sheight="[^"]*"', r'<svg\1', icon, count=1)
        icon = icon.replace("<svg", f'<svg x="{PAD + i * step:.2f}" y="{TOP}" width="{size}" height="{size}"', 1)
        parts.append(icon)
    groups = [
        ("Frameworks", "ASP.NET Core (Web API, MVC) · EF Core · ASP.NET Identity · SignalR · MediatR · FluentValidation · IHostedService"),
        ("Architecture", "Clean / Onion · DDD · CQRS · Modular Monolith · Outbox · Result Pattern · Repository & UoW · SOLID"),
        ("API & Reliability", "REST · Pagination · Idempotency · Optimistic Concurrency · Transactions · Swagger / OpenAPI"),
        ("Auth & Security", "JWT · Refresh-Token Rotation · Policy-Based Authorization · HMAC Webhook Verification"),
        ("Databases", "PostgreSQL (Npgsql) · SQL Server · MySQL · Redis · EF Core Migrations"),
        ("Testing", "xUnit · FluentAssertions · Integration Tests on PostgreSQL · NetArchTest"),
        ("Integrations", "Paymob · Stripe · Firebase Cloud Messaging · MailKit · SMS Gateways · AutoMapper · NLog"),
        ("DevOps & Tools", "Linux · nginx · systemd · Docker · Git · GitHub · Postman"),
    ]
    y0 = TOP + size + 32
    rh = 40
    for i, (label, values) in enumerate(groups):
        y = y0 + i * rh
        if i:
            parts.append(f'<rect x="{PAD}" y="{y}" width="{INNER}" height="1" fill="{STROKE}" opacity=".7"/>')
        parts.append(f'<text x="{PAD}" y="{y + 26}" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="1.2" fill="{LILAC}">{esc(label.upper())}</text>')
        parts.append(f'<text x="{PAD + 200}" y="{y + 26}" font-family="{SANS}" font-size="15" fill="{BODY}">{esc(values)}</text>')
    H = int(y0 + len(groups) * rh + PAD - 8)
    save("stack", panel("Tech Stack", "languages, frameworks and tools", H, "".join(parts)))


# ------------------------------------------------------------------ experience
def experience() -> None:
    entries = [
        ("Aug 2026 – Present", ".NET Backend Developer", "Takamol · Cairo, Egypt (Remote)",
         "Production ASP.NET Core APIs for web and mobile products. Built the Ahlena backend.", True),
        ("Mar 2025 – Present", ".NET Backend Developer (Freelance)", "Upwork / Mostaql · Remote",
         "APIs and C# automation for international clients, including a UK-based academy.", True),
        ("Jul 2023 – Mar 2025", "Mandatory Military Service", "Egypt", "", False),
        ("Sep 2019 – Jul 2023", "B.Sc. Computer Science", "Damanhur University",
         "ICPC community trainer · Google Developer Student Club Java instructor.", False),
        ("Mar 2021 – Oct 2021", ".NET Backend Developer", "ZATECH · Alexandria, Egypt",
         "REST APIs with ASP.NET Web API, Identity and JWT on SQL Server / MySQL.", False),
    ]
    row = 100
    dx = PAD + 222
    parts = [f'<rect x="{dx - 1}" y="{TOP + 10}" width="2" height="{(len(entries) - 1) * row}" fill="{STROKE}"/>']
    for i, (period, role, org, note, now) in enumerate(entries):
        y = TOP + i * row
        parts.append(f'<text x="{dx - 30}" y="{y + 16}" font-family="{MONO}" font-size="14" fill="{MUTED}" text-anchor="end" style="font-variant-ligatures:none">{esc(period)}</text>')
        if now:
            parts.append(f'<circle class="pulse" cx="{dx}" cy="{y + 11}" r="12" fill="{GREEN}" opacity=".22"/><circle cx="{dx}" cy="{y + 11}" r="6.5" fill="{GREEN}"/>')
        else:
            parts.append(f'<circle cx="{dx}" cy="{y + 11}" r="6.5" fill="#0D0A1A" stroke="{LILAC}" stroke-width="3"/>')
        parts.append(f'<text x="{dx + 32}" y="{y + 18}" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">{esc(role)}</text>')
        parts.append(f'<text x="{dx + 32}" y="{y + 44}" font-family="{SANS}" font-size="15" font-weight="600" fill="{LILAC}">{esc(org)}</text>')
        if note:
            parts.append(f'<text x="{dx + 32}" y="{y + 68}" font-family="{SANS}" font-size="15" fill="{MUTED}">{esc(note)}</text>')
    H = int(TOP + (len(entries) - 1) * row + 68 + PAD - 6)
    save("experience", panel("Experience", "work and education", H, "".join(parts),
                             style=".pulse{animation:pulse 2s ease-in-out infinite}@keyframes pulse{50%{opacity:.05}}"))


# ------------------------------------------------------------------ beyond the code
def beyond() -> None:
    gap = 24
    cw = (INNER - gap) / 2
    th = 230
    blocks = [
        ("RIGHT NOW", [("At work", "maintaining ASP.NET Core products"),
                       ("On GitHub", "TheZone and C# problem solving"),
                       ("Freelance", "APIs and C# automation for clients")]),
        ("OUTSIDE CLIENT WORK", [("ICPC", "ran university problem-solving sessions"),
                       ("GDSC", "taught Java, from basics to advanced topics"),
                       ("LeetCode", "my solutions are written in C#")]),
    ]
    parts = []
    for b, (label, rows) in enumerate(blocks):
        x = PAD + b * (cw + gap)
        parts.append(tile(x, TOP, cw, th))
        parts.append(f'<text x="{x + 28}" y="{TOP + 42}" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="1.6" fill="{LILAC}">{esc(label)}</text>')
        for i, (k, v) in enumerate(rows):
            y = TOP + 92 + i * 48
            parts.append(f'<rect x="{x + 28}" y="{y - 15}" width="3" height="20" rx="1.5" fill="url(#accent)"/>')
            parts.append(f'<text x="{x + 44}" y="{y}" font-family="{SANS}" font-size="16" fill="{MUTED}" xml:space="preserve"><tspan font-weight="700" fill="{TEXT}">{esc(k)}</tspan>  {esc(v)}</text>')
    H = int(TOP + th + PAD)
    save("beyond", panel("Beyond the Code", "current work and community", H, "".join(parts)))


# ------------------------------------------------------------------ footer
def footer() -> None:
    H = 232
    body = f"""
  <text x="{W / 2}" y="98" font-family="{SANS}" font-size="34" font-weight="700" fill="{TEXT}" text-anchor="middle">Want to <tspan fill="{LILAC}">get in touch?</tspan></text>
  <text x="{W / 2}" y="134" font-family="{SANS}" font-size="17" fill="{MUTED}" text-anchor="middle">For a .NET role, a freelance project, or a question about my work.</text>
  <rect x="{W / 2 - 40}" y="160" width="80" height="2" rx="1" fill="url(#accent)"/>
  <text x="{W / 2}" y="194" font-family="{MONO}" font-size="15" fill="{SOFT}" text-anchor="middle" xml:space="preserve">mosad55522@gmail.com   ·   +20 102 141 7408   ·   leetcode.com/u/Mossad</text>"""
    save("footer", panel("", "", H, body, label="Get in touch with Mossad Ahmed"))


if __name__ == "__main__":
    header()
    about()
    services()
    projects()
    stack()
    experience()
    beyond()
    footer()
    print("static panels written to", OUT)
