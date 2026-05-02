#!/usr/bin/env python3
"""
Erzeugt story-in-work/leseproben.html aus buch/leseproben/*.md.

Liest alle Leseproben, parst YAML-Header, konvertiert Markdown-Absätze zu HTML
und rendert eine Übersichtsseite im Story-in-Work-Design.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESEPROBEN_DIR = ROOT / "buch" / "leseproben"
OUT_FILE = ROOT / "story-in-work" / "leseproben.html"


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
            # Fortsetzung
            meta[current_key] += " " + line.strip()
    return meta, body


def md_to_html(text: str) -> str:
    """Minimaler Markdown-Renderer: Absätze, kursiv, fett, Dialog."""
    text = text.strip()

    # Entferne H1-Überschrift falls vorhanden (wir nutzen YAML-Titel)
    text = re.sub(r"^#\s+.*\n+", "", text)

    # Horizontal rule -> Szenen-Trenner
    text = re.sub(r"^---$", '<hr class="scene-break">', text, flags=re.MULTILINE)

    # Absätze
    paragraphs = re.split(r"\n\n+", text)
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith("<hr"):
            html_parts.append(p)
            continue
        # Inline: **fett** -> <strong>
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        # Inline: *kursiv* -> <em>  (aber nicht wenn im Wort)
        p = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?!\w)", r"<em>\1</em>", p)
        # Zeilenumbrüche innerhalb eines Absatzes (nur bei Dialog oft): weich durchlassen
        p = p.replace("\n", "<br>")
        html_parts.append(f"<p>{p}</p>")
    return "\n".join(html_parts)


def load_proben():
    """Alle Leseproben sortiert nach führender Nummer einlesen."""
    proben = []
    for md_file in sorted(LESEPROBEN_DIR.glob("*.md")):
        if md_file.name == "README.md":
            continue
        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        # Nummer + Slug aus Dateinamen
        m = re.match(r"^(\d+)-(.+)\.md$", md_file.name)
        if not m:
            continue
        nummer = int(m.group(1))
        slug = m.group(2)

        # Wortzahl
        wortzahl = len(re.findall(r"\b\w+\b", body))

        # Status-Check: wenn "ENTWURF —" im Body, ist es noch ein Skelett
        is_skeleton = body.lstrip().startswith("# ENTWURF") or "**Status:** Skizze" in body

        proben.append({
            "nummer": nummer,
            "slug": slug,
            "kategorie": meta.get("kategorie", ""),
            "pov": meta.get("pov", ""),
            "figuren": meta.get("figuren", ""),
            "register": meta.get("register", ""),
            "heat_level": meta.get("heat_level", ""),
            "primaer_referenz": meta.get("primaer_referenz", ""),
            "ergaenzende_referenz": meta.get("ergaenzende_referenz", ""),
            "zweck": meta.get("zweck", ""),
            "canon_status": meta.get("canon_status", ""),
            "body_html": md_to_html(body),
            "wortzahl": wortzahl,
            "is_skeleton": is_skeleton,
        })
    return proben


def render_html(proben):
    """HTML-Seite im Story-in-Work-Design rendern."""
    probe_cards = []
    total_words = 0
    total_ready = 0

    for p in proben:
        if not p["is_skeleton"]:
            total_ready += 1
            total_words += p["wortzahl"]

        nr_str = f"{p['nummer']:02d}"
        pov = p["pov"] or "—"
        heat = p["heat_level"] or "—"
        kategorie = p["kategorie"] or p["slug"]
        status_badge = "SKIZZE" if p["is_skeleton"] else "BEREIT"
        status_class = "sk" if p["is_skeleton"] else "ok"

        # Escape-Helper für Attribute
        def esc(s):
            return (s or "").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

        card = f'''
        <div class="probe-card" id="p-{nr_str}" data-nr="{nr_str}" data-kapid="lp{nr_str}" data-pov="{esc(pov)}" data-heat="{esc(heat)}" data-skeleton="{1 if p["is_skeleton"] else 0}" data-comments-loaded="0">
          <div class="probe-head">
            <div class="probe-left">
              <div class="probe-num">Nr. {nr_str}</div>
              <div class="probe-kat">{esc(kategorie)}</div>
            </div>
            <div class="probe-right">
              <div class="probe-meta">
                <span class="meta-pov">{esc(pov)}</span>
                <span class="meta-sep">·</span>
                <span class="meta-heat">{esc(heat)}</span>
              </div>
              <div class="probe-status s-{status_class}">{status_badge}</div>
              <div class="probe-arrow">&#x203A;</div>
            </div>
          </div>
          <div class="probe-body">
            <div class="probe-info">
              <dl>
                <dt>POV</dt><dd>{esc(p["pov"])}</dd>
                <dt>Figuren</dt><dd>{esc(p["figuren"])}</dd>
                <dt>Register</dt><dd>{esc(p["register"])}</dd>
                <dt>Heat</dt><dd>{esc(p["heat_level"])}</dd>
                <dt>Primär</dt><dd>{esc(p["primaer_referenz"])}</dd>
                <dt>Ergänzend</dt><dd>{esc(p["ergaenzende_referenz"])}</dd>
                <dt>Zweck</dt><dd>{esc(p["zweck"])}</dd>
                <dt>Wörter</dt><dd>{p["wortzahl"]}</dd>
              </dl>
            </div>
            <div class="probe-prosa">
              {p["body_html"]}
            </div>
          </div>
        </div>
        '''
        probe_cards.append(card)

    cards_html = "\n".join(probe_cards)
    total_count = len(proben)

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Der Riss — Leseproben</title>
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="/story-in-work/sidebar.css?v=20260502b">
  <script src="/story-in-work/sidebar.js?v=20260502b" defer></script>
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

    /* Probe-Karte */
    .probe-card {{
      background: var(--paper);
      border-radius: 2px 6px 6px 2px;
      box-shadow: 0 0 0 1px var(--paper-edge), 0 8px 28px rgba(0,0,0,0.25);
      margin-bottom: 1rem; overflow: hidden; position: relative;
    }}
    .probe-card::before {{
      content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
      background: linear-gradient(180deg, var(--paper-edge) 0%, #c8bfb0 50%, var(--paper-edge) 100%);
    }}
    .probe-card[data-skeleton="1"] {{ opacity: 0.55; }}
    .probe-card[data-skeleton="1"]::before {{
      background: linear-gradient(180deg, #d4cec2 0%, #b8ae9a 50%, #d4cec2 100%);
    }}

    .probe-head {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 1rem 1.5rem; cursor: pointer; user-select: none;
      border-bottom: 1px solid rgba(107,58,58,0.04);
      transition: background 0.2s;
      gap: 1rem;
    }}
    .probe-head:hover {{ background: rgba(107,58,58,0.02); }}
    .probe-left {{ display: flex; flex-direction: column; gap: 0.15rem; min-width: 0; flex: 1; }}
    .probe-num {{
      font-family: 'Inter', sans-serif; font-size: 0.6rem;
      letter-spacing: 0.25em; text-transform: uppercase; color: var(--smoke);
    }}
    .probe-kat {{
      font-family: 'Cormorant Garamond', serif; font-size: 1.05rem;
      font-weight: 400; color: var(--ink); line-height: 1.3;
    }}
    .probe-right {{ display: flex; align-items: center; gap: 1rem; flex-shrink: 0; }}
    .probe-meta {{
      font-family: 'Inter', sans-serif; font-size: 0.65rem;
      color: var(--muted); text-align: right; line-height: 1.5;
    }}
    .meta-sep {{ color: var(--smoke); margin: 0 0.3rem; }}
    .probe-status {{
      font-family: 'Inter', sans-serif; font-size: 0.58rem;
      letter-spacing: 0.1em; text-transform: uppercase;
      padding: 0.2rem 0.45rem; border-radius: 2px;
    }}
    .probe-status.s-ok {{ background: rgba(46,139,87,0.12); color: #2E8B57; }}
    .probe-status.s-sk {{ background: rgba(139,115,85,0.12); color: #8B7355; }}
    .probe-arrow {{ font-size: 1rem; color: var(--smoke); transition: transform 0.3s; }}
    .probe-head.open .probe-arrow {{ transform: rotate(90deg); }}

    .probe-body {{
      max-height: 0; overflow: hidden;
      transition: max-height 0.4s ease;
      background: #fbf7f0;
    }}
    .probe-body.open {{ max-height: 30000px; }}

    .probe-info {{
      padding: 1rem 1.5rem 0.5rem;
      border-bottom: 1px dashed rgba(107,58,58,0.12);
    }}
    .probe-info dl {{
      display: grid; grid-template-columns: 100px 1fr;
      gap: 0.25rem 1rem; margin: 0;
      font-family: 'Inter', sans-serif; font-size: 0.7rem;
    }}
    .probe-info dt {{ color: var(--smoke); letter-spacing: 0.05em; text-transform: uppercase; font-size: 0.6rem; padding-top: 0.15rem; }}
    .probe-info dd {{ margin: 0; color: var(--muted); line-height: 1.5; }}

    .probe-prosa {{
      padding: 1.2rem 2rem 2rem;
      font-family: 'Cormorant Garamond', serif;
      font-size: 1rem; line-height: 1.75; color: var(--ink);
    }}
    .probe-prosa p {{ margin: 0 0 0.9rem; position: relative; }}
    .probe-prosa em {{ font-style: italic; }}
    .probe-prosa strong {{ font-weight: 600; }}
    .probe-prosa hr.scene-break {{
      border: none; border-top: 1px solid rgba(107,58,58,0.2);
      width: 40%; margin: 1.5rem auto;
    }}

    /* ===== Comment UI (analog lesen/_reader.html) ===== */
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
    .probe-prosa p:hover .comment-trigger {{ opacity: 0.7; }}
    .probe-prosa p.has-comments .comment-trigger {{ opacity: 0.8; border-color: var(--accent); color: var(--accent); }}
    .probe-prosa p.has-comments {{ border-left: 2px solid var(--accent); padding-left: 0.6rem; margin-left: -0.8rem; }}

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

    .comment-quick-tags {{
      display: flex; flex-wrap: wrap; gap: 0.25rem;
      margin: 0.5rem 0 0.4rem 0;
    }}
    .comment-quick-tag {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase;
      background: none; border: 1px solid var(--smoke); color: var(--smoke);
      padding: 0.12rem 0.45rem; border-radius: 2px; cursor: pointer;
      transition: background 0.15s, color 0.15s, border-color 0.15s;
    }}
    .comment-quick-tag:hover:not(:disabled) {{ background: var(--accent); color: var(--paper); border-color: var(--accent); }}
    .comment-quick-tag.tag-gut {{ border-color: #6b8e6b; color: #6b8e6b; }}
    .comment-quick-tag.tag-gut:hover:not(:disabled) {{ background: #6b8e6b; border-color: #6b8e6b; color: var(--paper); }}
    .comment-quick-tag:disabled {{ opacity: 0.35; cursor: default; }}

    @media (max-width: 600px) {{
      .comment-trigger {{ right: -1.6rem; }}
      .probe-head {{ padding: 0.9rem 1.2rem; flex-wrap: wrap; }}
      .probe-meta {{ display: none; }}
      .probe-prosa {{ padding: 1rem 1.2rem 1.5rem; font-size: 0.95rem; }}
      .probe-info {{ padding: 0.8rem 1.2rem 0.4rem; }}
      .probe-info dl {{ grid-template-columns: 80px 1fr; }}
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
        <a href="/story-in-work/kanon.html" class="siw-link siw-sub" data-page="kanon">Kanon-Index</a>
        <a href="/canon/" class="siw-link siw-sub" data-page="canon">Kanon-Leser</a>
      </nav>
    </div>
  </aside>
  <button class="siw-burger" id="siw-burger" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
  <div class="siw-overlay" id="siw-overlay"></div>
  <div class="grain"></div>
  <div class="wrap">
    <div class="page-title">Der Riss — Leseproben</div>
    <div class="page-subtitle">Ton-Etüden für alle Register</div>
    <div class="page-desc">
      Jede Probe ist ein Register-Beispiel für einen Stilvektor des Positionings —
      Commercial Dark Fantasy, Commercial Romantasy, Commercial BDSM, dunkle Register für Krieg,
      Captivity, Mutilation und Trauer. Sie sind <strong>nicht Plot-Canon</strong>, sondern
      Kalibrierungs-Referenzen für <code>/entwurf</code>, <code>/ausarbeitung</code>, <code>/stil-check</code>,
      <code>/refit</code>, <code>/council</code>.
    </div>

    <div class="top-links">
      <a href="index.html">&larr; Kapitel</a>
      <span class="sep">·</span>
      <a href="kanon.html">Kanon</a>
      <span class="sep">·</span>
      <a href="charaktere.html">Figuren</a>
      <span class="sep">·</span>
      <a href="zeitleiste.html">Zeitleiste</a>
    </div>

    <div class="page-stats">
      <strong>{total_ready}</strong> / {total_count} bereit &middot; <strong>{total_words:,}</strong> Wörter Prosa
    </div>

    <div class="filter-bar" id="filter-bar">
      <button class="filter-btn active" data-filter="all">Alle</button>
      <button class="filter-btn" data-filter="ready">Bereit</button>
      <button class="filter-btn" data-filter="Alphina">Alphina</button>
      <button class="filter-btn" data-filter="Vesper">Vesper</button>
      <button class="filter-btn" data-filter="Maren">Maren</button>
      <button class="filter-btn" data-filter="Nyr">Nyr</button>
      <button class="filter-btn" data-filter="Varen">Varen</button>
      <button class="filter-btn" data-filter="Talven">Talven</button>
    </div>

    <div id="proben-list">
      {cards_html}
    </div>
  </div>

  <script>
    // ===== Comment-System (analog lesen/_reader.html) =====
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

    const QUICK_TAGS = [
      {{ label: 'ABSTRACT',  text: 'ABSTRACT — zu vage, kein konkretes Bild' }},
      {{ label: 'ERKLÄRT',   text: 'ERKLÄRT — Auswertung vor den Daten (announced interpretation)' }},
      {{ label: 'SCHARNIER', text: 'SCHARNIER — Aphorismus der erklärt was das Bild schon sagt' }},
      {{ label: 'GRAMMAR',   text: 'GRAMMAR — verquere oder gebrochene Satzkonstruktion' }},
      {{ label: 'REGISTER',  text: 'REGISTER — falsches POV-Vokabular, Berufslinse gebrochen' }},
      {{ label: 'RHYTHMUS',  text: 'RHYTHMUS — falsches Tempo für diese Szene' }},
      {{ label: 'BEGEHREN',  text: 'BEGEHREN — Attraction declared, nicht demonstrated' }},
      {{ label: 'GUT ✓',     text: 'GUT — sitzt, nicht anfassen', cls: 'tag-gut' }},
    ];

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

      const quickTagsDiv = document.createElement('div');
      quickTagsDiv.className = 'comment-quick-tags';
      QUICK_TAGS.forEach(tag => {{
        const btn = document.createElement('button');
        btn.className = 'comment-quick-tag' + (tag.cls ? ' ' + tag.cls : '');
        btn.textContent = tag.label;
        btn.onclick = async (e) => {{
          e.stopPropagation();
          btn.disabled = true;
          try {{
            await postComment(tag.text);
            closeActivePopup();
          }} catch (_) {{
            btn.disabled = false;
          }}
        }};
        quickTagsDiv.appendChild(btn);
      }});
      popup.appendChild(quickTagsDiv);

      const textarea = document.createElement('textarea');
      textarea.className = 'comment-textarea';
      textarea.placeholder = 'Oder freier Text …';
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
      const prosa = card.querySelector('.probe-prosa');
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

    // Toggle — beim Aufklappen Comments lazy laden
    document.querySelectorAll('.probe-head').forEach(head => {{
      head.addEventListener('click', () => {{
        head.classList.toggle('open');
        const card = head.closest('.probe-card');
        const body = head.nextElementSibling;
        if (body && body.classList.contains('probe-body')) {{
          body.classList.toggle('open');
          if (body.classList.contains('open') && card) {{
            initCommentsForCard(card);
          }}
        }}
      }});
    }});

    // Auto-open per URL-Hash (#p-XX) + scroll + Comments
    function openFromHash() {{
      const hash = window.location.hash;
      if (!hash || !hash.startsWith('#p-')) return;
      const card = document.querySelector(hash);
      if (!card) return;
      const head = card.querySelector('.probe-head');
      const body = card.querySelector('.probe-body');
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
    const cards = Array.from(document.querySelectorAll('.probe-card'));
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
        }} else if (f === 'ready') {{
          show = card.dataset.skeleton === '0';
        }} else {{
          // POV-Filter
          show = (card.dataset.pov || '').toLowerCase().includes(f.toLowerCase());
        }}
        card.style.display = show ? '' : 'none';
      }});
    }});
  </script>
</body>
</html>
'''


def main():
    if not LESEPROBEN_DIR.exists():
        print(f"FEHLER: {LESEPROBEN_DIR} nicht gefunden", file=sys.stderr)
        return 1

    proben = load_proben()
    if not proben:
        print("WARNUNG: keine Leseproben gefunden")
        return 0

    html = render_html(proben)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(html, encoding="utf-8")

    ready = sum(1 for p in proben if not p["is_skeleton"])
    words = sum(p["wortzahl"] for p in proben if not p["is_skeleton"])
    print(f"build-leseproben: {ready}/{len(proben)} Proben bereit, {words} Wörter Prosa → {OUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
