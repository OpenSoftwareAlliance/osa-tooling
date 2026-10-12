#!/usr/bin/env python3
"""Gera o README padronizado de cada repo OSA.

Uso: python3 .osa/readme.py [repo ...]   (sem argumentos: todos)
Escreve <repo>/README.md (respeitando o nome existente, ex.: readme.md).
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORG = "https://github.com/OpenSoftwareAlliance"

# repo: (features, current stack)
DETAILS = {
    "pad": (["Real-time co-editing with per-author colors", "Full revision history with timeslider", "Comments, chat and import/export (HTML, TXT, DOCX/PDF via LibreOffice)", "Plugin system and 100+ languages"], "Node.js + TypeScript, Socket.IO, ueberDB (SQLite/Postgres/MySQL)"),
    "sheet": (["Excel-like grid with formulas and formatting", "Charts, pivot tables, conditional formatting", "Freeze panes, filters, sorting", "Collaboration through a pluggable backend"], "JavaScript (jQuery), frontend-only library"),
    "cal": (["Public booking pages and event types", "Calendar sync (Google, Outlook, CalDAV)", "Team round-robin and collective scheduling", "Workflows, webhooks and 100+ app integrations"], "Next.js + TypeScript, Prisma + Postgres, Turborepo"),
    "mail": (["Email forwarding for custom domains", "Aliases, catch-all and regex rules", "Domain verification (MX, SPF, DKIM, DMARC)", "Dashboard and REST API"], "Node.js (Koa), Pug, MongoDB, Redis"),
    "meet": (["Peer-to-peer video rooms, no account needed", "End-to-end encrypted WebRTC streams", "Screen sharing and chat", "Installable PWA, multi-language"], "Vue + TypeScript (Vite), WebRTC, Node signaling server"),
    "draw": (["Infinite canvas whiteboard", "Shapes, arrows, text, images and frames", "Real-time multiplayer", "SDK to embed the canvas in other apps"], "React + TypeScript monorepo, Cloudflare Workers + Durable Objects"),
    "drop": (["Send files between devices on the same network", "Peer-to-peer over WebRTC, nothing stored on the server", "Text messages between devices", "Installable PWA, no sign-up"], "Vanilla JS client, Node.js WebSocket signaling server"),
    "share": (["One-click and drag-and-drop uploads, no registration", "Temporary or permanent file links", "File type and size limits, blacklists", "API for scripts and ShareX"], "PHP, SQLite/MySQL/Postgres"),
    "share-admin": (["Upload stats and storage usage", "Search files by hash, name or IP", "Delete or blacklist files", "Bulk actions per uploader IP"], "PHP, shares the OSA Share database"),
    "bin": (["Zero-knowledge pastes encrypted in the browser (AES-256-GCM)", "Expiration, burn-after-reading and passwords", "Discussions, file attachments and syntax highlighting", "QR codes and multiple storage backends"], "PHP + JavaScript, filesystem/SQL/S3/GCS storage"),
    "snip": (["Create and share code snippets and gists", "Syntax highlighting and Markdown rendering", "Private, unlisted and password-protected posts", "Multiple files per post"], "Next.js App Router + TypeScript, Prisma + Postgres"),
    "short": (["Short links with custom domains and aliases", "Click statistics (browsers, OS, countries, referrers)", "Password-protected and expiring links", "REST API and user accounts"], "Node.js (Express) + Handlebars/htmx, Knex (Postgres/MySQL/SQLite), Redis"),
    "alias": (["Domain redirects configured only through DNS records", "Path and wildcard redirect rules", "Automatic HTTPS via Let's Encrypt", "No accounts, no dashboard"], "Go"),
    "page": (["Link-in-bio pages with custom themes", "Drag-and-drop link ordering", "Analytics for page views and clicks", "Custom domains"], "Next.js + TypeScript, Tailwind, GraphQL"),
    "feedback": (["Public feedback boards and voting", "Roadmaps and changelog", "Roles and permissions", "Comments and status updates"], "Vue + TypeScript, Node.js (Express), Postgres"),
    "jam": (["Live audio rooms for small and large groups", "Speakers, moderators and audience roles", "Room links that work in the browser", "Self-hostable SFU for large rooms"], "JavaScript (React UI), Node.js + Redis, mediasoup SFU"),
    "micro": (["Catalog of ready-to-use micro service APIs", "OpenAPI specs for each service", "Dashboard and API explorer", "Client examples"], "Next.js + TypeScript dashboard, Go services"),
    "username": (["Check username availability on 100+ sites", "Results streamed as you type", "Direct links to each profile", "Lightweight single-page app"], "React (Create React App)"),
    "osa-desktop": (["Dynamic Island: music, calendar, timers, downloads and shelf", "Volume mixer and audio routing", "System monitor and fan control", "Window management and app switcher", "Clipboard history and snippets", "Screen capture and recording"], "Swift 6 / AppKit + SwiftUI, macOS 14+ Apple Silicon"),
    "status": (["Uptime monitoring of every OSA service", "Public status page", "Incident reports as GitHub issues", "Response-time graphs"], "Upptime (GitHub Actions, Issues and Pages)"),
}

# Repos whose local directory (and GitHub repo, until renamed) differs from the manifest key.
DIRS = {"osa-desktop": "vorssaint-utils"}

# Repos with fixed roadmap links instead of the landscape/migration issues: (label, url) list.
ROADMAP = {
    "osa-desktop": [
        ("Roadmap", "docs/specs/ROADMAP.md"),
        ("Rebrand tracking issue", "https://github.com/OpenSoftwareAlliance/vorssaint-utils/issues/21"),
    ],
}

# Native macOS apps: no Cloudflare migration target and no self-hosting section.
NATIVE = {"osa-desktop"}

EXTRA = {
    "status": ("OSA Status", "Uptime monitor and status page for the OSA services.", "-", "Upptime", "https://github.com/upptime/upptime", "MIT"),
}


def load_manifest():
    rows = {}
    with open(os.path.join(ROOT, ".osa", "repos.tsv")) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            r, product, tagline, alt, upname, upurl, lic = line.rstrip("\n").split("\t")
            rows[r] = (product, tagline, alt, upname, upurl, lic)
    rows.update(EXTRA)
    return rows


def readme_path(repo):
    d = os.path.join(ROOT, DIRS.get(repo, repo))
    for name in os.listdir(d):
        if name.lower() == "readme.md":
            return os.path.join(d, name)
    return os.path.join(d, "README.md")


def load_issues():
    out = {}
    with open(os.path.join(ROOT, ".osa", "issues.tsv")) as f:
        for line in f:
            r, kind, url = line.rstrip("\n").split("\t")
            out[(r, kind.split(".")[0])] = url
    return out


ISSUES = load_issues()


def render(repo, rows):
    product, tagline, alt, upname, upurl, lic = rows[repo]
    features, stack = DETAILS[repo]
    alt_txt = f"Open source alternative to **{alt}**." if alt != "-" else "Part of the open source suite."
    if repo in NATIVE:
        alt_txt = ""
    if repo in NATIVE:
        stack_block = f"- {stack}"
        roadmap = "\n".join(f"- [{l}]({u})" for l, u in ROADMAP[repo]) + f"\n- [All issues]({ORG}/{repo}/issues)"
        install = f"""## Build from source

```sh
git clone {ORG}/{repo}.git
cd {repo}
./build.sh --dev
```

Xcode Command Line Tools are the only requirement. Release builds are unsigned unless `OSA_TEAM_ID` is set, so the app does not install updates itself: it opens the release page instead. Download builds from the [Releases page]({ORG}/{repo}/releases)."""
        credit = f"{product} is based on [{upname}]({upurl}). Credit for the original work goes to its authors. See [NOTICE](NOTICE)."
    else:
        land = ISSUES[(repo, "landscape")]
        mig = ISSUES[(repo, "migration")]
        stack_block = f"- **Current:** {stack}\n- **Target:** Next.js + TypeScript on Cloudflare Workers (see [migration research]({mig}))"
        roadmap = f"- [Open source landscape research]({land})\n- [Migration research: React/Next.js + TypeScript on Cloudflare Workers]({mig})\n- [All issues]({ORG}/{repo}/issues)"
        install = f"## Self-hosting\n\nInstallation and configuration follow the upstream project for now: see the [{upname} documentation]({upurl}#readme)."
        credit = f"{product} is based on [{upname}]({upurl}). Credit for the original work goes to its authors."
    lead = f"{alt_txt} Part of the [Open Software Alliance]({ORG}) suite.".strip()
    suite = "\n".join(
        f"| [{p}]({ORG}/{r}) | {t} | {a if a != '-' else '-'} |"
        for r, (p, t, a, *_rest) in rows.items()
    )
    feats = "\n".join(f"- {x}" for x in features)
    return f"""<div align="center">

# {product}

**{tagline}**

{lead}

</div>

---

## Features

{feats}

## Tech stack

{stack_block}

## Roadmap

{roadmap}

{install}

## The OSA suite

| Product | What it does | Alternative to |
|---|---|---|
{suite}

## License and credits

{credit}

License: {lic}. See the [LICENSE](LICENSE) file in this repository.
"""


def main():
    rows = load_manifest()
    targets = sys.argv[1:] or list(rows)
    for repo in targets:
        with open(readme_path(repo), "w") as f:
            f.write(render(repo, rows))
        print("readme ok:", repo)


if __name__ == "__main__":
    main()
