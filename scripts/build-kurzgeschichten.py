#!/usr/bin/env python3
"""
Erzeugt kurzgeschichten/index.html aus buch/kurzgeschichten/*.md.

Liest alle Kurzgeschichten (Würfel-Output von /kurzgeschichte), parst YAML-Header,
konvertiert Markdown-Absätze zu HTML und rendert eine reduzierte Übersichtsseite:
nur Seitentitel + Liste der Geschichten, keine Sidebar, keine Filter.

Dateinamen-Pattern: YYYYMMDD-{slug}.md (z.B. 20260506-vesper-maren-werft.md).
README.md wird übersprungen.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KG_DIR = ROOT / "buch" / "kurzgeschichten"
OUT_DIR = ROOT / "kurzgeschichten"
OUT_FILE = OUT_DIR / "index.html"


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
            "figuren": meta.get("figuren", ""),
            "welt": meta.get("welt", ""),
            "ort": meta.get("ort", ""),
            "body_html": md_to_html(body),
            "wortzahl": wortzahl,
        })
    return geschichten


def render_html(geschichten):
    """HTML-Seite ohne Sidebar/Filter — nur Titel + Liste."""
    cards = []

    for g in geschichten:
        slug_id = f"kg-{g['datum']}-{g['slug']}" if g["datum"] else f"kg-{g['slug']}"
        kapid = slug_id

        def esc(s):
            return (s or "").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

        card = f'''
        <article class="kg-card" id="{slug_id}" data-kapid="{kapid}" data-comments-loaded="0">
          <header class="kg-head">
            <div class="kg-date">{esc(g["datum"])}</div>
            <h2 class="kg-titel">{esc(g["titel"])}</h2>
            <div class="kg-meta">
              <span>{esc(g["figuren"])}</span>
              <span class="meta-sep">·</span>
              <span>{esc(g["ort"])}</span>
              <span class="meta-sep">·</span>
              <span>{g["wortzahl"]} W</span>
            </div>
          </header>
          <div class="kg-prosa">
            {g["body_html"]}
          </div>
        </article>
        '''
        cards.append(card)

    cards_html = "\n".join(cards) if cards else '<p class="kg-empty">Noch keine Geschichten.</p>'

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Kurzgeschichten</title>
  <style>
    :root {{
      --ink: #1e1c19; --muted: #6b6259;
      --accent: #6b3a3a; --deep: #0f0e0c; --smoke: #8a8279;
      --paper: #f8f4ee; --paper-edge: #e8e0d4;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      background: var(--deep); color: var(--paper);
      font-family: 'Cormorant Garamond', Georgia, serif;
      margin: 0; padding: 3rem 1.5rem 5rem;
      min-height: 100vh; display: flex; justify-content: center;
    }}
    .wrap {{ width: 100%; max-width: 760px; }}

    .page-title {{
      text-align: center;
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 2.4rem; font-weight: 400; letter-spacing: 0.05em;
      color: var(--paper); margin: 0 0 3rem;
    }}

    .kg-card {{
      background: var(--paper); color: var(--ink);
      border-radius: 2px;
      box-shadow: 0 0 0 1px var(--paper-edge), 0 4px 16px rgba(0,0,0,0.3);
      margin-bottom: 2rem; padding: 2rem 2.5rem;
    }}
    .kg-head {{
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid rgba(107,58,58,0.2);
    }}
    .kg-date {{
      font-family: 'Inter', sans-serif; font-size: 0.65rem;
      letter-spacing: 0.25em; text-transform: uppercase; color: var(--smoke);
      margin-bottom: 0.4rem;
    }}
    .kg-titel {{
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 1.6rem; font-weight: 400; line-height: 1.2;
      color: var(--ink); margin: 0 0 0.6rem;
    }}
    .kg-meta {{
      font-family: 'Inter', sans-serif; font-size: 0.7rem;
      color: var(--muted); letter-spacing: 0.03em;
    }}
    .meta-sep {{ color: var(--smoke); margin: 0 0.4rem; }}

    .kg-prosa {{
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 1.05rem; line-height: 1.75; color: var(--ink);
    }}
    .kg-prosa p {{ margin: 0 0 1rem; position: relative; }}
    .kg-prosa em {{ font-style: italic; }}
    .kg-prosa strong {{ font-weight: 600; }}
    .kg-prosa h2.kg-section {{
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 0.75rem; letter-spacing: 0.3em; text-transform: uppercase;
      color: var(--smoke); margin: 2rem 0 1rem; font-weight: 400;
      border-bottom: 1px solid rgba(107,58,58,0.15);
      padding-bottom: 0.3rem;
    }}
    .kg-prosa hr.scene-break {{
      border: none; border-top: 1px solid rgba(107,58,58,0.2);
      width: 40%; margin: 1.5rem auto;
    }}

    .kg-empty {{
      text-align: center; color: var(--smoke); font-style: italic;
      padding: 3rem 1rem;
    }}

    /* Comment UI (analog Leseproben) */
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
      font-family: 'Cormorant Garamond', Georgia, serif;
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
      font-family: 'Cormorant Garamond', Georgia, serif; font-size: 0.95rem;
      background: var(--paper); border: 1px solid var(--smoke);
      border-radius: 3px; padding: 0.5rem; color: var(--ink);
      resize: vertical; min-height: 4rem; margin-top: 0.5rem;
    }}
    .comment-submit {{
      margin-top: 0.4rem;
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 0.8rem; letter-spacing: 0.15em; text-transform: uppercase;
      background: none; border: 1px solid var(--accent); color: var(--accent);
      padding: 0.3rem 0.9rem; border-radius: 2px; cursor: pointer;
      transition: background 0.2s, color 0.2s;
    }}
    .comment-submit:hover {{ background: var(--accent); color: var(--paper); }}
    .comment-submit:disabled {{ opacity: 0.4; cursor: default; }}

    @media (max-width: 600px) {{
      body {{ padding: 2rem 0.8rem 4rem; }}
      .page-title {{ font-size: 1.8rem; margin-bottom: 2rem; }}
      .kg-card {{ padding: 1.5rem 1.2rem; }}
      .kg-titel {{ font-size: 1.3rem; }}
      .kg-prosa {{ font-size: 1rem; }}
      .comment-trigger {{ right: -1.6rem; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1 class="page-title">Kurzgeschichten</h1>
    {cards_html}
  </div>

  <script>
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

    // Comments fuer alle Cards laden (alle ausgeklappt sichtbar)
    document.querySelectorAll('.kg-card').forEach(card => initCommentsForCard(card));

    // Auto-scroll bei Hash
    function scrollFromHash() {{
      const hash = window.location.hash;
      if (!hash || !hash.startsWith('#kg-')) return;
      const card = document.querySelector(hash);
      if (!card) return;
      setTimeout(() => card.scrollIntoView({{ behavior: 'smooth', block: 'start' }}), 50);
    }}
    scrollFromHash();
    window.addEventListener('hashchange', scrollFromHash);
  </script>
</body>
</html>
'''


def main():
    if not KG_DIR.exists():
        print("build-kurzgeschichten: 0 Geschichten (Ordner leer oder nicht vorhanden)")
        return 0

    geschichten = load_geschichten()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = render_html(geschichten)
    OUT_FILE.write_text(html, encoding="utf-8")

    if not geschichten:
        print(f"build-kurzgeschichten: 0 Geschichten — leere Seite gerendert → {OUT_FILE.relative_to(ROOT)}")
        return 0

    words = sum(g["wortzahl"] for g in geschichten)
    print(f"build-kurzgeschichten: {len(geschichten)} Geschichten, {words} Wörter → {OUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
