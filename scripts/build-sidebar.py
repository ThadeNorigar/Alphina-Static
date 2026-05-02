#!/usr/bin/env python3
"""
Injiziert das Sidebar-Markup in alle relevanten Pages.

Sucht in jeder Page das <body>-Tag und ersetzt es plus alles bis zum
naechsten Marker (oder bis zum naechsten direkten Body-Child) durch:
  <body class="siw-with-sidebar">
    [Sidebar-Markup]
    <-- Marker SIDEBAR_END -->
    [Originaler Body-Inhalt nach dem Marker]

Bei Erstlauf (kein Marker) wird das Markup direkt nach <body> eingefuegt
und der SIDEBAR_END-Marker dahinter gesetzt.

Aufruf:  python scripts/build-sidebar.py
"""

from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pages, in die das Sidebar-Markup injiziert wird.
# Alle Pages, die aus der Sidebar verlinkt sind, brauchen die Sidebar selbst —
# sonst verschwindet die Navigation beim Klick.
INCLUDE_PAGES = [
    ROOT / "story-in-work" / "index.html",
    ROOT / "story-in-work" / "kanon.html",
    ROOT / "story-in-work" / "charaktere.html",
    ROOT / "story-in-work" / "zeitleiste.html",
    ROOT / "story-in-work" / "moragh-karte.html",
    ROOT / "canon" / "index.html",
    ROOT / "status" / "index.html",
    ROOT / "story" / "index.html",
    ROOT / "architektur.html",
]

EXCLUDE_PAGES: list[Path] = []

SIDEBAR_START = "<!-- SIDEBAR_START (build-sidebar.py — nicht haendisch editieren) -->"
SIDEBAR_END = "<!-- SIDEBAR_END -->"

SIDEBAR_HTML = """
  <aside class="siw-sidebar" id="siw-sidebar">
    <div class="siw-sidebar-inner">
      <a href="/story-in-work/index.html" class="siw-brand">DER RISS</a>
      <nav class="siw-nav">
        <a href="/story-in-work/index.html" class="siw-link" data-page="siw-index">Trilogie</a>
        <a href="/story-in-work/zeitleiste.html" class="siw-link" data-page="zeitleiste">Zeitleiste</a>
        <a href="/architektur.html" class="siw-link" data-page="architektur">Architektur</a>
        <a href="/status/" class="siw-link" data-page="status">Kapitel-Status</a>
        <div class="siw-section">Layer 1 — Welt</div>
        <a href="/canon/?doc=00-welt" class="siw-link siw-sub">Weltbibel</a>
        <a href="/story-in-work/moragh-karte.html" class="siw-link siw-sub" data-page="moragh-karte">Moragh-Karte</a>
        <a href="/canon/?doc=00-canon-kompakt" class="siw-link siw-sub">Kanon kompakt</a>
        <div class="siw-section">Layer 2 — Regeln</div>
        <a href="/canon/?doc=01-autorin-stimme" class="siw-link siw-sub">Autorin-Stimme</a>
        <a href="/canon/?doc=02-stilregeln-v2" class="siw-link siw-sub">Stilregeln</a>
        <a href="/canon/?doc=01-referenz-konkretheit" class="siw-link siw-sub">Konkretheit</a>
        <a href="/canon/?doc=10-magie-system" class="siw-link siw-sub">Magie-System</a>
        <a href="/canon/?doc=20-moragh-talente" class="siw-link siw-sub">Moragh-Talente</a>
        <a href="/canon/?doc=18-thar-magitech" class="siw-link siw-sub">Thar-Magitech</a>
        <div class="siw-section">Layer 3 — Figuren</div>
        <a href="/story-in-work/charaktere.html" class="siw-link siw-sub" data-page="charaktere">Hauptfiguren</a>
        <a href="/canon/?doc=21-moragh-gesellschaft" class="siw-link siw-sub">Fraktionen</a>
        <a href="/canon/?doc=22-moragh-figuren" class="siw-link siw-sub">Nebenfiguren-Index</a>
        <div class="siw-section">Layer 4 — Story</div>
        <a href="/canon/?doc=00-storyline" class="siw-link siw-sub">Trilogie-Bogen</a>
        <a href="/canon/?doc=synopse-b1" class="siw-link siw-sub">Synopse Buch 1</a>
        <a href="/canon/?doc=synopse-b2" class="siw-link siw-sub">Synopse Buch 2</a>
        <a href="/canon/?doc=synopse-b3" class="siw-link siw-sub">Synopse Buch 3</a>
        <a href="/canon/?doc=12-buch3-konzept" class="siw-link siw-sub">Buch 3 — Konzept</a>
        <div class="siw-section">Layer 6 — Aktpläne</div>
        <a href="/canon/?doc=02-akt1" class="siw-link siw-sub">B1 Akt I–IV</a>
        <a href="/canon/?doc=06-buch2-akt1" class="siw-link siw-sub">B2 Akt I–IV</a>
        <a href="/canon/?doc=14-buch3-akt1" class="siw-link siw-sub">B3 Akt I–IV</a>
        <div class="siw-section">Material</div>
        <a href="/story-in-work/leseproben.html" class="siw-link siw-sub" data-page="leseproben">Leseproben</a>
        <a href="/story-in-work/kanon.html" class="siw-link siw-sub" data-page="kanon">Kanon-Index</a>
        <a href="/canon/" class="siw-link siw-sub" data-page="canon">Kanon-Leser</a>
      </nav>
    </div>
  </aside>
  <button class="siw-burger" id="siw-burger" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
  <div class="siw-overlay" id="siw-overlay"></div>
"""


def remove_all_sidebar_blocks(content: str) -> str:
    """Entfernt ALLE Sidebar-Spuren — markierte und unmarkierte."""
    # 1. Markierte Block(e)
    content = re.sub(
        r"\n?" + re.escape(SIDEBAR_START) + r".*?" + re.escape(SIDEBAR_END),
        "",
        content,
        flags=re.DOTALL,
    )
    # 2. Unmarkierte <aside class="siw-sidebar">...</aside>
    content = re.sub(
        r'\s*<aside\s+class="siw-sidebar"[^>]*>.*?</aside>',
        "",
        content,
        flags=re.DOTALL,
    )
    # 3. Burger
    content = re.sub(
        r'\s*<button\s+class="siw-burger"[^>]*>.*?</button>',
        "",
        content,
        flags=re.DOTALL,
    )
    # 4. Overlay
    content = re.sub(
        r'\s*<div\s+class="siw-overlay"[^>]*>\s*</div>',
        "",
        content,
        flags=re.DOTALL,
    )
    return content


SIDEBAR_LINK_TAG = '<link rel="stylesheet" href="/story-in-work/sidebar.css?v=20260502e">'
SIDEBAR_SCRIPT_TAG = '<script src="/story-in-work/sidebar.js?v=20260502e" defer></script>'


def ensure_css_js_tags(content: str) -> str:
    """Fuegt sidebar.css/js-Tags in <head> ein, falls noch nicht da. Updated v=... falls schon da."""
    has_css = re.search(r'<link[^>]*sidebar\.css', content) is not None
    has_js = re.search(r'<script[^>]*sidebar\.js', content) is not None

    # Bestehende Tags auf aktuellen Cache-Bust updaten
    content = re.sub(
        r'<link[^>]*sidebar\.css[^>]*>',
        SIDEBAR_LINK_TAG,
        content,
    )
    content = re.sub(
        r'<script[^>]*sidebar\.js[^>]*></script>',
        SIDEBAR_SCRIPT_TAG,
        content,
    )

    # Falls Tags fehlten, vor </head> einfuegen
    if not has_css or not has_js:
        new_tags = []
        if not has_css:
            new_tags.append("  " + SIDEBAR_LINK_TAG)
        if not has_js:
            new_tags.append("  " + SIDEBAR_SCRIPT_TAG)
        content = re.sub(
            r"(\s*</head>)",
            "\n" + "\n".join(new_tags) + r"\1",
            content,
            count=1,
        )

    return content


def inject(content: str) -> str:
    """Setzt body class, entfernt alte Sidebar-Spuren, injiziert frisches Markup + CSS/JS-Tags."""
    # 1. CSS/JS-Tags sicherstellen
    content = ensure_css_js_tags(content)

    # 2. Body-Class setzen
    content = re.sub(
        r'<body(?:\s+class="([^"]*)")?>',
        lambda m: '<body class="siw-with-sidebar">'
        if not m.group(1)
        else (
            f'<body class="{m.group(1)}">'
            if "siw-with-sidebar" in m.group(1)
            else f'<body class="{m.group(1)} siw-with-sidebar">'
        ),
        content,
        count=1,
    )

    # 3. Alle alten Sidebar-Spuren raus
    content = remove_all_sidebar_blocks(content)

    # 4. Frisches Markup nach <body...>
    block = f"{SIDEBAR_START}{SIDEBAR_HTML}{SIDEBAR_END}"
    content = re.sub(
        r"(<body[^>]*>)",
        r"\1\n" + block,
        content,
        count=1,
    )

    return content


def strip(content: str) -> str:
    """Entfernt Sidebar-Markup (markiert + unmarkiert), body-Class und sidebar.css/js-Tags."""
    # 1. Alle Sidebar-Spuren raus
    content = remove_all_sidebar_blocks(content)

    # 2. body-Class siw-with-sidebar entfernen
    def fix_body(m: re.Match) -> str:
        cls = m.group(1)
        new_cls = " ".join(c for c in cls.split() if c != "siw-with-sidebar").strip()
        if new_cls:
            return f'<body class="{new_cls}">'
        return "<body>"

    content = re.sub(r'<body\s+class="([^"]*)">', fix_body, content, count=1)

    # 3. sidebar.css/js Link- und Script-Tags entfernen (mit oder ohne ?v=...)
    content = re.sub(
        r'\s*<link[^>]+href="[^"]*sidebar\.css[^"]*"[^>]*>\s*\n?',
        "\n",
        content,
    )
    content = re.sub(
        r'\s*<script[^>]+src="[^"]*sidebar\.js[^"]*"[^>]*>\s*</script>\s*\n?',
        "\n",
        content,
    )

    return content


def main() -> None:
    print("Sidebar-Build:")
    for page in INCLUDE_PAGES:
        if not page.exists():
            print(f"  SKIP (fehlt): {page.relative_to(ROOT)}")
            continue
        original = page.read_text(encoding="utf-8")
        updated = inject(original)
        if updated == original:
            print(f"  unchanged: {page.relative_to(ROOT)}")
        else:
            page.write_text(updated, encoding="utf-8")
            print(f"  injected:  {page.relative_to(ROOT)}")

    print()
    print("Sidebar-Strip (Pages außerhalb /story-in-work/):")
    for page in EXCLUDE_PAGES:
        if not page.exists():
            print(f"  SKIP (fehlt): {page.relative_to(ROOT)}")
            continue
        original = page.read_text(encoding="utf-8")
        updated = strip(original)
        if updated == original:
            print(f"  clean:     {page.relative_to(ROOT)}")
        else:
            page.write_text(updated, encoding="utf-8")
            print(f"  stripped:  {page.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
