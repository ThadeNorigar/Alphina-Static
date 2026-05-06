#!/usr/bin/env python3
"""
Erzeugt story-in-work/kurzgeschichten.html aus buch/kurzgeschichten/*.md.

Liest alle Kurzgeschichten (Würfel-Output von /kurzgeschichte), parst YAML-Header,
konvertiert Markdown-Absätze zu HTML und rendert eine Übersichtsseite im
Story-in-Work-Design.

Dateinamen-Pattern: YYYYMMDD-{slug}.md (z.B. 20260506-vesper-maren-werft.md).
README.md wird übersprungen.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KG_DIR = ROOT / "buch" / "kurzgeschichten"
OUT_FILE = ROOT / "story-in-work" / "kurzgeschichten.html"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """YAML-Frontmatter aus Markdown extrahieren. Minimal — keine externe Abhängigkeit."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    raw = parts[1].strip()
    body = parts[2].lstrip("\n")

    meta = {}
    current_key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip()
            meta[current_key] = val
        elif current_key and line.startswith(" "):
            meta[current_key] += " " + line.strip()
    return meta, body


def md_to_html(text: str) -> str:
    """Minimaler Markdown-Renderer: H1/H2, Absätze, kursiv, fett."""
    text = text.strip()

    # H1 in der Body extrahieren als Titel — wir nutzen ihn separat, entfernen aus Body
    text = re.sub(r"^#\s+.*\n+", "", text, count=1)

    # H2 -> Subheading-Stil
    text = re.sub(r"^##\s+(.+)$", r'<h2 class="kg-section">\1</h2>', text, flags=re.MULTILINE)

    # Horizontal rule -> Szenen-Trenner
    text = re.sub(r"^---$", '<hr class="scene-break">', text, flags=re.MULTILINE)

    # Absätze
    paragraphs = re.split(r"\n\n+", text)
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<h2") or p.startswith("<hr"):
            html_parts.append(p)
            continue
        # Inline: **fett** -> <strong>
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        # Inline: *kursiv* -> <em>
        p = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?!\w)", r"<em>\1</em>", p)
        # Zeilenumbrüche innerhalb eines Absatzes
        p = p.replace("\n", "<br>")
        html_parts.append(f"<p>{p}</p>")
    return "\n".join(html_parts)


def extract_title(body: str, slug: str) -> str:
    """H1-Titel aus Body extrahieren, sonst Slug-zu-Titel."""
    m = re.match(r"^#\s+(.+)$", body.strip(), flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    return slug.replace("-", " ").title()


def load_geschichten():
    """Alle Kurzgeschichten sortiert nach Datum (neueste zuerst) einlesen."""
    geschichten = []
    if not KG_DIR.exists():
        return geschichten

    for md_file in sorted(KG_DIR.glob("*.md"), reverse=True):
        if md_file.name == "README.md":
            continue
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        # Pattern: YYYYMMDD-{slug}.md
        m = re.match(r"^(\d{8})-(.+)\.md$", md_file.name)
        if not m:
            # Falls jemand ohne Datum schreibt, akzeptieren wir's trotzdem
            datum = ""
            slug = md_file.stem
        else:
            datum_raw = m.group(1)
            datum = f"{datum_raw[:4]}-{datum_raw[4:6]}-{datum_raw[6:8]}"
            slug = m.group(2)

        wortzahl = len(re.findall(r"\b\w+\b", body))
        titel = extract_title(body, slug)

        geschichten.append({
            "datum": datum,
            "slug": slug,
            "titel": titel,
            "typ": meta.get("typ", ""),
            "canon_status": meta.get("canon_status", ""),
            "figuren": meta.get("figuren", ""),
            "welt": meta.get("welt", ""),
            "ort": meta.get("ort", ""),
            "tageszeit": meta.get("tageszeit", ""),
            "monat": meta.get("monat", ""),
            "witterung": meta.get("witterung", ""),
            "begegnungs_anlass": meta.get("begegnungs_anlass", ""),
            "akt_sets": meta.get("akt_sets", ""),
            "heat_level": meta.get("heat_level", ""),
            "laenge": meta.get("laenge", ""),
            "body_html": md_to_html(body),
            "wortzahl": wortzahl,
        })
    return geschichten


def heat_class(heat: str) -> str:
    h = (heat or "").lower()
    if "bdsm" in h:
        return "bdsm"
    if "tantra" in h or "slow" in h:
        return "tantra"
    if "heat" in h or "explizit" in h:
        return "heat"
    return "other"


def render_html(geschichten):
    """HTML-Seite im Story-in-Work-Design rendern."""
    cards = []
    total_words = 0

    for g in geschichten:
        total_words += g["wortzahl"]
        slug_id = f"kg-{g['datum']}-{g['slug']}" if g["datum"] else f"kg-{g['slug']}"
        kapid = slug_id  # für Comment-System

        def esc(s):
            return (s or "").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

        h_class = heat_class(g["heat_level"])

        card = f'''
        <div class="kg-card" id="{slug_id}" data-kapid="{kapid}" data-welt="{esc(g["welt"])}" data-heat="{h_class}" data-figuren="{esc(g["figuren"])}" data-comments-loaded="0">
          <div class="kg-head">
            <div class="kg-left">
              <div class="kg-date">{esc(g["datum"])}</div>
              <div class="kg-titel">{esc(g["titel"])}</div>
            </div>
            <div class="kg-right">
              <div class="kg-meta">
                <span class="meta-figuren">{esc(g["figuren"])}</span>
                <span class="meta-sep">·</span>
                <span class="meta-welt">{esc(g["welt"])}</span>
              </div>
              <div class="kg-heat heat-{h_class}">{esc(g["heat_level"])}</div>
              <div class="kg-arrow">&#x203A;</div>
            </div>
          </div>
          <div class="kg-body">
            <div class="kg-info">
              <dl>
                <dt>Figuren</dt><dd>{esc(g["figuren"])}</dd>
                <dt>Welt</dt><dd>{esc(g["welt"])}</dd>
                <dt>Ort</dt><dd>{esc(g["ort"])}</dd>
                <dt>Zeit</dt><dd>{esc(g["tageszeit"])} · {esc(g["monat"])} · {esc(g["witterung"])}</dd>
                <dt>Anlass</dt><dd>{esc(g["begegnungs_anlass"])}</dd>
                <dt>Akt-Sets</dt><dd>{esc(g["akt_sets"])}</dd>
                <dt>Heat</dt><dd>{esc(g["heat_level"])}</dd>
                <dt>Wörter</dt><dd>{g["wortzahl"]}</dd>
              </dl>
            </div>
            <div class="kg-prosa">
              {g["body_html"]}
            </div>
          </div>
        </div>
        '''
        cards.append(card)

    cards_html = "\n".join(cards)
    total_count = len(geschichten)

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Der Riss — Kurzgeschichten</title>
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="/story-in-work/sidebar.css?v=20260506a">
  <script src="/story-in-work/sidebar.js?v=20260506a" defer></script>
  <style>
    :root {{
      --cream: #f5f0e8; --ink: #1e1c19; --muted: #6b6259;
      --accent: #6b3a3a; --deep: #0f0e0c; --smoke: #8a8279;
      --paper: #f8f4ee; --paper-edge: #e8e0d4;
    }}
    body {{
      background: var(--deep); display: flex; justify-content: center;
      padding: 2rem 1rem; min-height: 100vh;
    }}
    nav {{ display: none; }}
    .wrap {{ width: 100%; max-width: 820px; }}

    .page-title {{
      text-align: center; padding: 1rem 0 0.3rem;
      font-family: 'Cormorant Garamond', serif; font-size: 0.7rem;
      letter-spacing: 0.4em; text-transform: uppercase; color: var(--smoke);
    }}
    .page-subtitle {{
      text-align: center; padding: 0 0 0.8rem;
      font-family: 'Cormorant Garamond', serif; font-size: 0.95rem;
      color: var(--paper-edge); letter-spacing: 0.05em;
    }}
    .page-desc {{
      text-align: center; padding: 0 2rem 1.2rem;
      font-family: 'Inter', sans-serif; font-size: 0.72rem;
      color: var(--smoke); line-height: 1.7; max-width: 640px; margin: 0 auto;
    }}
    .page-stats {{
      text-align: center; padding: 0 0 1.5rem;
      font-family: 'Inter', sans-serif; font-size: 0.7rem;
      color: var(--smoke); letter-spacing: 0.05em;
    }}
    .page-stats strong {{ color: var(--paper-edge); }}

    .top-links {{
      text-align: center; padding: 0 0 1.5rem;
      font-family: 'Cormorant Garamond', serif; font-size: 0.85rem;
      letter-spacing: 0.1em;
    }}
    .top-links a {{
      color: var(--paper-edge); text-decoration: none;
      border-bottom: 1px solid var(--smoke);
      padding-bottom: 2px; transition: all 0.3s;
    }}
    .top-links a:hover {{ color: var(--accent); border-bottom-color: var(--accent); }}
    .top-links .sep {{ color: var(--smoke); margin: 0 0.6rem; }}

    /* Filter-Leiste */
    .filter-bar {{
      display: flex; gap: 0.6rem; flex-wrap: wrap; justify-content: center;
      padding: 0 0 1.5rem;
    }}
    .filter-btn {{
      font-family: 'Inter', sans-serif; font-size: 0.65rem;
      letter-spacing: 0.08em; text-transform: uppercase;
      padding: 0.35rem 0.8rem; border: 1px solid var(--smoke);
      background: transparent; color: var(--paper-edge);
      cursor: pointer; border-radius: 2px; transition: all 0.2s;
    }}
    .filter-btn:hover {{ border-color: var(--paper-edge); color: #fff; }}
    .filter-btn.active {{ background: var(--accent); border-color: var(--accent); color: var(--paper); }}

    /* Kurzgeschichte-Karte */
    .kg-card {{
      background: var(--paper);
      border-radius: 2px 6px 6px 2px;
      box-shadow: 0 0 0 1px var(--paper-edge), 0 8px 28px rgba(0,0,0,0.25);
      margin-bottom: 1rem; overflow: hidden; position: relative;
    }}
    .kg-card::before {{
      content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
      background: linear-gradient(180deg, var(--paper-edge) 0%, #c8bfb0 50%, var(--paper-edge) 100%);
    }}

    .kg-head {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 1rem 1.5rem; cursor: pointer; user-select: none;
      border-bottom: 1px solid rgba(107,58,58,0.04);
      transition: background 0.2s;
      gap: 1rem;
    }}
    .kg-head:hover {{ background: rgba(107,58,58,0.02); }}
    .kg-left {{ display: flex; flex-direction: column; gap: 0.15rem; min-width: 0; flex: 1; }}
    .kg-date {{
      font-family: 'Inter', sans-serif; font-size: 0.6rem;
      letter-spacing: 0.25em; text-transform: uppercase; color: var(--smoke);
    }}
    .kg-titel {{
      font-family: 'Cormorant Garamond', serif; font-size: 1.05rem;
      font-weight: 400; color: var(--ink); line-height: 1.3;
    }}
    .kg-right {{ display: flex; align-items: center; gap: 1rem; flex-shrink: 0; }}
    .kg-meta {{
      font-family: 'Inter', sans-serif; font-size: 0.65rem;
      color: var(--muted); text-align: right; line-height: 1.5;
      max-width: 200px;
    }}
    .meta-sep {{ color: var(--smoke); margin: 0 0.3rem; }}
    .kg-heat {{
      font-family: 'Inter', sans-serif; font-size: 0.58rem;
      letter-spacing: 0.08em;
      padding: 0.2rem 0.45rem; border-radius: 2px;
      max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }}
    .kg-heat.heat-bdsm {{ background: rgba(139,58,58,0.18); color: #8b3a3a; }}
    .kg-heat.heat-heat {{ background: rgba(184,116,82,0.18); color: #a85f3a; }}
    .kg-heat.heat-tantra {{ background: rgba(70,110,70,0.18); color: #4f7a4f; }}
    .kg-heat.heat-other {{ background: rgba(139,115,85,0.12); color: #8B7355; }}
    .kg-arrow {{ font-size: 1rem; color: var(--smoke); transition: transform 0.3s; }}
    .kg-head.open .kg-arrow {{ transform: rotate(90deg); }}

    .kg-body {{
      max-height: 0; overflow: hidden;
      transition: max-height 0.4s ease;
      background: #fbf7f0;
    }}
    .kg-body.open {{ max-height: 30000px; }}

    .kg-info {{
      padding: 1rem 1.5rem 0.5rem;
      border-bottom: 1px dashed rgba(107,58,58,0.12);
    }}
    .kg-info dl {{
      display: grid; grid-template-columns: 100px 1fr;
      gap: 0.25rem 1rem; margin: 0;
      font-family: 'Inter', sans-serif; font-size: 0.7rem;
    }}
    .kg-info dt {{ color: var(--smoke); letter-spacing: 0.05em; text-transform: uppercase; font-size: 0.6rem; padding-top: 0.15rem; }}
    .kg-info dd {{ margin: 0; color: var(--muted); line-height: 1.5; }}

    .kg-prosa {{
      padding: 1.2rem 2rem 2rem;
      font-family: 'Cormorant Garamond', serif;
      font-size: 1rem; line-height: 1.75; color: var(--ink);
    }}
    .kg-prosa p {{ margin: 0 0 0.9rem; position: relative; }}
    .kg-prosa em {{ font-style: italic; }}
    .kg-prosa strong {{ font-weight: 600; }}
    .kg-prosa h2.kg-section {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 0.75rem; letter-spacing: 0.3em; text-transform: uppercase;
      color: var(--smoke); margin: 1.5rem 0 0.8rem; font-weight: 400;
      border-bottom: 1px solid rgba(107,58,58,0.15);
      padding-bottom: 0.3rem;
    }}
    .kg-prosa hr.scene-break {{
      border: none; border-top: 1px solid rgba(107,58,58,0.2);
      width: 40%; margin: 1.5rem auto;
    }}

    /* ===== Comment UI (analog leseproben.html) ===== */
    .comment-trigger {{
      position: absolute; right: -2.2rem; top: 0.25em;
      width: 1.4rem; height: 1.4rem;
      background: none; border: 1px solid var(--paper-edge);
      border-radius: 50%; cursor: pointer;
      opacity: 0.25; transition: opacity 0.2s, border-color 0.2s, color 0.2s;
      font-size: 0.65rem;
      display: flex; align-items: center; justify-content: center;
      color: var(--smoke); padding: 0; line-height: 1;
    }}
    .comment-trigger:hover {{ opacity: 1; border-color: var(--accent); color: var(--accent); }}
    .kg-prosa p:hover .comment-trigger {{ opacity: 0.7; }}
    .kg-prosa p.has-comments .comment-trigger {{ opacity: 0.8; border-color: var(--accent); color: var(--accent); }}
    .kg-prosa p.has-comments {{ border-left: 2px solid var(--accent); padding-left: 0.6rem; margin-left: -0.8rem; }}

    .comment-popup {{
      position: relative;
      margin: 0.5rem 0 1rem 0;
      background: var(--paper-edge);
      border: 1px solid var(--smoke);
      border-radius: 4px;
      padding: 0.8rem 1rem;
      font-family: 'Cormorant Garamond', serif;
      font-size: 0.9rem;
    }}
    .comment-popup-close {{
      position: absolute; top: 0.4rem; right: 0.6rem;
      background: none; border: none; cursor: pointer;
      font-size: 1.1rem; color: var(--smoke); line-height: 1;
    }}
    .comment-list {{ margin-bottom: 0.6rem; }}
    .comment-item {{
      padding: 0.4rem 0;
      border-bottom: 1px solid rgba(107,58,58,0.15);
      color: var(--ink); line-height: 1.5;
    }}
    .comment-item:last-child {{ border-bottom: none; }}
    .comment-item-meta {{
      font-size: 0.72rem; color: var(--smoke);
      letter-spacing: 0.05em; margin-top: 0.2rem;
    }}
    .comment-empty {{
      color: var(--smoke); font-style: italic;
      font-size: 0.85rem; margin-bottom: 0.4rem;
    }}
    .comment-textarea {{
      width: 100%; box-sizing: border-box;
      font-family: 'Cormorant Garamond', serif; font-size: 0.95rem;
      background: var(--paper); border: 1px solid var(--smoke);
      border-radius: 3px; padding: 0.5rem; color: var(--ink);
      resize: vertical; min-height: 4rem; margin-top: 0.5rem;
    }}
    .comment-submit {{
      margin-top: 0.4rem;
      font-family: 'Cormorant Garamond', serif;
      font-size: 0.8rem; letter-spacing: 0.15em; text-transform: uppercase;
      background: none; border: 1px solid var(--accent); color: var(--accent);
      padding: 0.3rem 0.9rem; border-radius: 2px; cursor: pointer;
      transition: background 0.2s, color 0.2s;
    }}
    .comment-submit:hover {{ background: var(--accent); color: var(--paper); }}
    .comment-submit:disabled {{ opacity: 0.4; cursor: default; }}

    @media (max-width: 600px) {{
      .comment-trigger {{ right: -1.6rem; }}
      .kg-head {{ padding: 0.9rem 1.2rem; flex-wrap: wrap; }}
      .kg-meta {{ display: none; }}
      .kg-prosa {{ padding: 1rem 1.2rem 1.5rem; font-size: 0.95rem; }}
      .kg-info {{ padding: 0.8rem 1.2rem 0.4rem; }}
      .kg-info dl {{ grid-template-columns: 80px 1fr; }}
    }}
  </style>
</head>
<body class="siw-with-sidebar">
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
        <a href="/story-in-work/kurzgeschichten.html" class="siw-link siw-sub siw-active" data-page="kurzgeschichten">Kurzgeschichten</a>
        <a href="/story-in-work/kanon.html" class="siw-link siw-sub" data-page="kanon">Kanon-Index</a>
        <a href="/canon/" class="siw-link siw-sub" data-page="canon">Kanon-Leser</a>
      </nav>
    </div>
  </aside>
  <button class="siw-burger" id="siw-burger" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
  <div class="siw-overlay" id="siw-overlay"></div>
  <div class="grain"></div>
  <div class="wrap">
    <div class="page-title">Der Riss — Kurzgeschichten</div>
    <div class="page-subtitle">Würfel-Output: Setting · Begegnung · Akt</div>
    <div class="page-desc">
      Zufalls-Kombinationen aus Figuren, Welt, Begegnungs-Anlass und drei Akt-Sets
      aus dem Anatomie-Register. Stil-Übungen, <strong>kein Plot-Canon</strong>,
      keine Kaskade in Zeitleiste oder Status. Generiert via <code>/kurzgeschichte</code>.
    </div>

    <div class="top-links">
      <a href="index.html">&larr; Trilogie</a>
      <span class="sep">·</span>
      <a href="leseproben.html">Leseproben</a>
      <span class="sep">·</span>
      <a href="charaktere.html">Figuren</a>
      <span class="sep">·</span>
      <a href="zeitleiste.html">Zeitleiste</a>
    </div>

    <div class="page-stats">
      <strong>{total_count}</strong> Geschichten &middot; <strong>{total_words:,}</strong> Wörter
    </div>

    <div class="filter-bar" id="filter-bar">
      <button class="filter-btn active" data-filter="all">Alle</button>
      <button class="filter-btn" data-filter="welt:Thalassien">Thalassien</button>
      <button class="filter-btn" data-filter="welt:Moragh">Moragh</button>
      <button class="filter-btn" data-filter="heat:heat">Heat</button>
      <button class="filter-btn" data-filter="heat:bdsm">BDSM</button>
      <button class="filter-btn" data-filter="heat:tantra">Tantra</button>
      <button class="filter-btn" data-filter="fig:Alphina">Alphina</button>
      <button class="filter-btn" data-filter="fig:Sorel">Sorel</button>
      <button class="filter-btn" data-filter="fig:Vesper">Vesper</button>
      <button class="filter-btn" data-filter="fig:Maren">Maren</button>
    </div>

    <div id="kg-list">
      {cards_html}
    </div>
  </div>

  <script>
    // ===== Comment-System =====
    const COMMENT_API = '/api/comments';
    const COMMENT_MODUS = 'entwurf';
    let activePopup = null;

    function getUserId() {{
      let uid = localStorage.getItem('alphina_reader_id');
      if (!uid) {{
        uid = (crypto.randomUUID ? crypto.randomUUID()
               : Date.now().toString(36) + Math.random().toString(36).slice(2));
        localStorage.setItem('alphina_reader_id', uid);
      }}
      return uid;
    }}
    const USER_ID = getUserId();

    function escHtml(s) {{
      return String(s).replace(/[&<>"']/g, c => ({{
        '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
      }})[c]);
    }}

    function formatDate(iso) {{
      const d = new Date(iso);
      return d.toLocaleDateString('de-DE', {{ day: '2-digit', month: '2-digit', year: '2-digit' }})
        + ' ' + d.toLocaleTimeString('de-DE', {{ hour: '2-digit', minute: '2-digit' }});
    }}

    function closeActivePopup() {{
      if (activePopup) {{ activePopup.remove(); activePopup = null; }}
    }}

    function renderPopup(p, idx, kapId, commentsByIdx) {{
      closeActivePopup();
      const popup = document.createElement('div');
      popup.className = 'comment-popup';
      popup.dataset.idx = idx;

      const closeBtn = document.createElement('button');
      closeBtn.className = 'comment-popup-close';
      closeBtn.textContent = '×';
      closeBtn.onclick = closeActivePopup;
      popup.appendChild(closeBtn);

      const list = document.createElement('div');
      list.className = 'comment-list';
      const existing = commentsByIdx[idx] || [];
      if (existing.length === 0) {{
        list.innerHTML = '<p class="comment-empty">Noch keine Anmerkungen.</p>';
      }} else {{
        existing.forEach(c => {{
          const item = document.createElement('div');
          item.className = 'comment-item';
          item.innerHTML = '<div>' + escHtml(c.text) + '</div><div class="comment-item-meta">' + formatDate(c.created_at) + '</div>';
          list.appendChild(item);
        }});
      }}
      popup.appendChild(list);

      async function postComment(text) {{
        const absatzText = p.textContent.slice(0, 120);
        const r = await fetch(COMMENT_API, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json', 'X-User-Id': USER_ID }},
          body: JSON.stringify({{ kapitel_id: kapId, modus: COMMENT_MODUS, absatz_idx: idx, absatz_text: absatzText, text }}),
        }});
        if (!r.ok) throw new Error('Fehler ' + r.status);
        if (!commentsByIdx[idx]) commentsByIdx[idx] = [];
        commentsByIdx[idx].push({{ text, created_at: new Date().toISOString() }});
        p.classList.add('has-comments');
      }}

      const textarea = document.createElement('textarea');
      textarea.className = 'comment-textarea';
      textarea.placeholder = 'Anmerkung schreiben …';
      popup.appendChild(textarea);

      const submitBtn = document.createElement('button');
      submitBtn.className = 'comment-submit';
      submitBtn.textContent = 'Anmerken';
      submitBtn.onclick = async () => {{
        const text = textarea.value.trim();
        if (!text) return;
        submitBtn.disabled = true;
        submitBtn.textContent = '…';
        try {{
          await postComment(text);
          closeActivePopup();
          renderPopup(p, idx, kapId, commentsByIdx);
        }} catch (e) {{
          submitBtn.disabled = false;
          submitBtn.textContent = 'Fehler — nochmal';
        }}
      }};
      popup.appendChild(submitBtn);

      p.insertAdjacentElement('afterend', popup);
      activePopup = popup;
      textarea.focus();
    }}

    function initCommentsForCard(card) {{
      if (card.dataset.commentsLoaded === '1') return;
      card.dataset.commentsLoaded = '1';

      const kapId = card.dataset.kapid;
      const prosa = card.querySelector('.kg-prosa');
      if (!prosa) return;

      const commentsByIdx = {{}};

      fetch(COMMENT_API + '?kapitel=' + encodeURIComponent(kapId) + '&modus=' + COMMENT_MODUS, {{
        headers: {{ 'X-User-Id': USER_ID }}
      }})
        .then(r => r.json())
        .then(comments => {{
          comments.forEach(c => {{
            if (!commentsByIdx[c.absatz_idx]) commentsByIdx[c.absatz_idx] = [];
            commentsByIdx[c.absatz_idx].push(c);
          }});

          const paras = prosa.querySelectorAll('p');
          paras.forEach((p, idx) => {{
            const btn = document.createElement('button');
            btn.className = 'comment-trigger';
            btn.title = 'Anmerkung';
            btn.textContent = '✎';
            btn.onclick = (e) => {{
              e.stopPropagation();
              if (activePopup && activePopup.parentElement === prosa && parseInt(activePopup.dataset.idx) === idx) {{
                closeActivePopup();
              }} else {{
                renderPopup(p, idx, kapId, commentsByIdx);
              }}
            }};
            p.appendChild(btn);

            if (commentsByIdx[idx] && commentsByIdx[idx].length > 0) {{
              p.classList.add('has-comments');
            }}
          }});
        }})
        .catch(() => {{}});
    }}

    document.addEventListener('click', (e) => {{
      if (activePopup && !activePopup.contains(e.target) && !e.target.classList.contains('comment-trigger')) {{
        closeActivePopup();
      }}
    }});

    // Toggle
    document.querySelectorAll('.kg-head').forEach(head => {{
      head.addEventListener('click', () => {{
        head.classList.toggle('open');
        const card = head.closest('.kg-card');
        const body = head.nextElementSibling;
        if (body && body.classList.contains('kg-body')) {{
          body.classList.toggle('open');
          if (body.classList.contains('open') && card) {{
            initCommentsForCard(card);
          }}
        }}
      }});
    }});

    // Auto-open per URL-Hash
    function openFromHash() {{
      const hash = window.location.hash;
      if (!hash || !hash.startsWith('#kg-')) return;
      const card = document.querySelector(hash);
      if (!card) return;
      const head = card.querySelector('.kg-head');
      const body = card.querySelector('.kg-body');
      if (head && body && !body.classList.contains('open')) {{
        head.classList.add('open');
        body.classList.add('open');
        initCommentsForCard(card);
      }}
      setTimeout(() => card.scrollIntoView({{ behavior: 'smooth', block: 'start' }}), 50);
    }}
    openFromHash();
    window.addEventListener('hashchange', openFromHash);

    // Filter
    const filterBar = document.getElementById('filter-bar');
    const cards = Array.from(document.querySelectorAll('.kg-card'));
    filterBar.addEventListener('click', (e) => {{
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      filterBar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;
      cards.forEach(card => {{
        let show = true;
        if (f === 'all') {{
          show = true;
        }} else if (f.startsWith('welt:')) {{
          const w = f.slice(5).toLowerCase();
          show = (card.dataset.welt || '').toLowerCase().includes(w);
        }} else if (f.startsWith('heat:')) {{
          show = card.dataset.heat === f.slice(5);
        }} else if (f.startsWith('fig:')) {{
          show = (card.dataset.figuren || '').toLowerCase().includes(f.slice(4).toLowerCase());
        }}
        card.style.display = show ? '' : 'none';
      }});
    }});
  </script>
</body>
</html>
'''


def main():
    if not KG_DIR.exists():
        # Stille Beendigung — kein Fehler, wenn der Ordner noch leer ist
        print("build-kurzgeschichten: 0 Geschichten (Ordner leer oder nicht vorhanden)")
        return 0

    geschichten = load_geschichten()
    if not geschichten:
        # Trotzdem leere Index-Seite rendern, damit der Sidebar-Link nicht 404
        html = render_html([])
        OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUT_FILE.write_text(html, encoding="utf-8")
        print("build-kurzgeschichten: 0 Geschichten — leere Seite gerendert")
        return 0

    html = render_html(geschichten)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(html, encoding="utf-8")

    words = sum(g["wortzahl"] for g in geschichten)
    print(f"build-kurzgeschichten: {len(geschichten)} Geschichten, {words} Wörter → {OUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
