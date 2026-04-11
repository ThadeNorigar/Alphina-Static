# Alphina Kommentarsystem Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Per-Absatz Kommentarfunktion für alphina.net WIP-Seiten, anonym, gespeichert auf dem Server via FastAPI + SQLite.

**Architecture:** Neuer Docker-Container `alphina-comments` mit FastAPI + SQLite läuft im Caddy-Netzwerk. Caddy bekommt eine `/api/*`-Route für alphina.net. `_reader.html` bekommt eine Comment-UI die nur im `?wip`-Modus aktiv ist.

**Tech Stack:** Python 3.12-slim, FastAPI, uvicorn, SQLite (stdlib), Docker, Caddy v2, Vanilla JS

---

## File Map

| Datei | Aktion | Zweck |
|---|---|---|
| `/home/adrian/apps/alphina-comments/server.py` | Erstellen (SSH) | FastAPI App mit SQLite |
| `/home/adrian/apps/alphina-comments/Dockerfile` | Erstellen (SSH) | Container-Image |
| `/home/adrian/apps/alphina-comments/docker-compose.yml` | Erstellen (SSH) | Container starten + Netzwerk |
| `/home/adrian/docker/caddy/Caddyfile` | Ändern (SSH) | `/api/*` Route für alphina.net |
| `lesen/_reader.html` | Ändern (lokal) | Comment-UI im Frontend |

---

## Task 1: FastAPI Comment Server

**Files:**
- Create: `/home/adrian/apps/alphina-comments/server.py`

- [ ] **Schritt 1: Verzeichnis anlegen**

```bash
ssh adrian@adrianphilipp.de "mkdir -p ~/apps/alphina-comments"
```

- [ ] **Schritt 2: server.py erstellen**

```bash
ssh adrian@adrianphilipp.de "cat > ~/apps/alphina-comments/server.py" << 'PYEOF'
import sqlite3
import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

DB_PATH = os.environ.get("DB_PATH", "/data/comments.db")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://alphina.net"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                kapitel_id  TEXT    NOT NULL,
                modus       TEXT    NOT NULL DEFAULT 'entwurf',
                absatz_idx  INTEGER NOT NULL,
                absatz_text TEXT    NOT NULL DEFAULT '',
                text        TEXT    NOT NULL,
                created_at  TEXT    NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_kapitel ON comments(kapitel_id, modus)")
        conn.commit()


init_db()


class CommentIn(BaseModel):
    kapitel_id: str
    modus: str
    absatz_idx: int
    absatz_text: str
    text: str

    @field_validator("kapitel_id")
    @classmethod
    def validate_kapitel(cls, v: str) -> str:
        if len(v) > 10:
            raise ValueError("kapitel_id zu lang")
        return v

    @field_validator("modus")
    @classmethod
    def validate_modus(cls, v: str) -> str:
        if v not in ("entwurf", "final"):
            raise ValueError("modus muss 'entwurf' oder 'final' sein")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("text darf nicht leer sein")
        if len(v) > 2000:
            raise ValueError("text zu lang (max 2000 Zeichen)")
        return v

    @field_validator("absatz_text")
    @classmethod
    def validate_absatz_text(cls, v: str) -> str:
        return v[:120]

    @field_validator("absatz_idx")
    @classmethod
    def validate_idx(cls, v: int) -> int:
        if v < 0 or v > 10000:
            raise ValueError("absatz_idx ungültig")
        return v


@app.get("/api/comments")
def get_comments(kapitel: str, modus: str = "entwurf"):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, absatz_idx, absatz_text, text, created_at FROM comments "
            "WHERE kapitel_id = ? AND modus = ? ORDER BY absatz_idx, created_at",
            (kapitel, modus),
        ).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/comments", status_code=201)
def post_comment(body: CommentIn):
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            "INSERT INTO comments (kapitel_id, modus, absatz_idx, absatz_text, text, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (body.kapitel_id, body.modus, body.absatz_idx, body.absatz_text, body.text, now),
        )
        conn.commit()
    return {"ok": True}
PYEOF
```

- [ ] **Schritt 3: Prüfen**

```bash
ssh adrian@adrianphilipp.de "cat ~/apps/alphina-comments/server.py | head -5"
```

Erwartet: `import sqlite3`

---

## Task 2: Dockerfile + Docker Compose

**Files:**
- Create: `/home/adrian/apps/alphina-comments/Dockerfile`
- Create: `/home/adrian/apps/alphina-comments/docker-compose.yml`

- [ ] **Schritt 1: Dockerfile erstellen**

```bash
ssh adrian@adrianphilipp.de "cat > ~/apps/alphina-comments/Dockerfile" << 'EOF'
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic
COPY server.py .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

- [ ] **Schritt 2: docker-compose.yml erstellen**

Wichtig: Container muss im selben Docker-Netzwerk wie Caddy sein (`caddy_default`).

```bash
ssh adrian@adrianphilipp.de "cat > ~/apps/alphina-comments/docker-compose.yml" << 'EOF'
services:
  alphina-comments:
    build: .
    container_name: alphina-comments
    restart: unless-stopped
    environment:
      DB_PATH: /data/comments.db
    volumes:
      - /home/adrian/data/alphina-comments:/data
    networks:
      - caddy_default

networks:
  caddy_default:
    external: true
EOF
```

- [ ] **Schritt 3: Daten-Verzeichnis und Container starten**

```bash
ssh adrian@adrianphilipp.de "mkdir -p ~/data/alphina-comments && cd ~/apps/alphina-comments && docker compose up -d --build"
```

- [ ] **Schritt 4: Logs prüfen**

```bash
ssh adrian@adrianphilipp.de "docker logs alphina-comments"
```

Erwartet: `Application startup complete.`

- [ ] **Schritt 5: Intern testen (im Docker-Netz)**

```bash
ssh adrian@adrianphilipp.de "docker run --rm --network caddy_default curlimages/curl curl -s 'http://alphina-comments:8000/api/comments?kapitel=17&modus=entwurf'"
```

Erwartet: `[]`

---

## Task 3: Caddyfile — Route für /api/*

**Files:**
- Modify: `/home/adrian/docker/caddy/Caddyfile`

- [ ] **Schritt 1: Backup**

```bash
ssh adrian@adrianphilipp.de "cp ~/docker/caddy/Caddyfile ~/docker/caddy/Caddyfile.bak"
```

- [ ] **Schritt 2: alphina.net-Block ersetzen**

Aktueller Block:
```
alphina.net {
	import security_headers
	root * /srv/alphina-static
	file_server
}
```

Neuer Block:
```
alphina.net {
	import security_headers

	route /api/* {
		reverse_proxy alphina-comments:8000
	}

	root * /srv/alphina-static
	file_server
}
```

```bash
ssh adrian@adrianphilipp.de "sed -i 's|import security_headers\n\troot \* /srv/alphina-static\n\tfile_server|import security_headers\n\n\troute /api/* {\n\t\treverse_proxy alphina-comments:8000\n\t}\n\n\troot * /srv/alphina-static\n\tfile_server|' ~/docker/caddy/Caddyfile"
```

Da sed mit Newlines schwierig ist: Python verwenden:

```bash
ssh adrian@adrianphilipp.de "python3 - << 'PYEOF'
path = '/home/adrian/docker/caddy/Caddyfile'
old = '''alphina.net {
\timport security_headers
\troot * /srv/alphina-static
\tfile_server
}'''
new = '''alphina.net {
\timport security_headers

\troute /api/* {
\t\treverse_proxy alphina-comments:8000
\t}

\troot * /srv/alphina-static
\tfile_server
}'''
content = open(path).read()
assert old in content, 'Block nicht gefunden!'
open(path, 'w').write(content.replace(old, new))
print('ok')
PYEOF"
```

- [ ] **Schritt 3: Caddy neu laden**

```bash
ssh adrian@adrianphilipp.de "docker exec caddy caddy reload --config /etc/caddy/Caddyfile"
```

Erwartet: keine Fehler

- [ ] **Schritt 4: Extern testen**

```bash
curl -s "https://alphina.net/api/comments?kapitel=17&modus=entwurf"
```

Erwartet: `[]`

---

## Task 4: Frontend — Comment-UI in _reader.html

**Files:**
- Modify: `lesen/_reader.html`

Die UI ist nur aktiv wenn `isWip === true`. Kommentare werden pro Absatz-Index gespeichert.

- [ ] **Schritt 1: CSS für Comment-UI hinzufügen**

In `_reader.html` direkt vor `</style>` einfügen:

```css
/* ===== Comment UI (nur WIP-Modus) ===== */
.prose p { position: relative; }

.comment-trigger {
  position: absolute;
  right: -2rem;
  top: 0.2em;
  width: 1.4rem;
  height: 1.4rem;
  background: none;
  border: 1px solid var(--paper-edge);
  border-radius: 50%;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
  font-size: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--smoke);
  padding: 0;
  line-height: 1;
}
.comment-trigger:hover { border-color: var(--accent); color: var(--accent); }
.prose p:hover .comment-trigger { opacity: 1; }
.prose p.has-comments .comment-trigger { opacity: 0.6; border-color: var(--accent); color: var(--accent); }
.prose p.has-comments { border-left: 2px solid var(--accent); padding-left: 0.6rem; margin-left: -0.8rem; }

.comment-popup {
  position: relative;
  margin: 0.5rem 0 1rem 0;
  background: var(--warm);
  border: 1px solid var(--paper-edge);
  border-radius: 4px;
  padding: 0.8rem 1rem;
  font-family: 'Cormorant Garamond', serif;
  font-size: 0.9rem;
}
.comment-popup-close {
  position: absolute;
  top: 0.4rem; right: 0.6rem;
  background: none; border: none;
  cursor: pointer; font-size: 1rem;
  color: var(--smoke); line-height: 1;
}
.comment-list { margin-bottom: 0.6rem; }
.comment-item {
  padding: 0.4rem 0;
  border-bottom: 1px solid var(--paper-edge);
  color: var(--ink);
  line-height: 1.5;
}
.comment-item:last-child { border-bottom: none; }
.comment-item-meta {
  font-size: 0.72rem;
  color: var(--smoke);
  letter-spacing: 0.05em;
  margin-top: 0.2rem;
}
.comment-empty {
  color: var(--smoke);
  font-style: italic;
  font-size: 0.85rem;
  margin-bottom: 0.4rem;
}
.comment-textarea {
  width: 100%;
  box-sizing: border-box;
  font-family: 'Cormorant Garamond', serif;
  font-size: 0.95rem;
  background: var(--paper);
  border: 1px solid var(--paper-edge);
  border-radius: 3px;
  padding: 0.5rem;
  color: var(--ink);
  resize: vertical;
  min-height: 4rem;
  margin-top: 0.5rem;
}
.comment-submit {
  margin-top: 0.4rem;
  font-family: 'Cormorant Garamond', serif;
  font-size: 0.8rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  background: none;
  border: 1px solid var(--accent);
  color: var(--accent);
  padding: 0.3rem 0.9rem;
  border-radius: 2px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.comment-submit:hover { background: var(--accent); color: var(--paper); }
.comment-submit:disabled { opacity: 0.4; cursor: default; }
```

- [ ] **Schritt 2: JavaScript für Comment-UI hinzufügen**

Direkt vor `</script>` am Ende von `_reader.html` einfügen:

```javascript
// ===== Comment UI (nur WIP-Modus) =====
if (isWip) {
  const COMMENT_API = '/api/comments';
  const commentsByIdx = {}; // absatz_idx -> [{text, created_at}]
  let activePopup = null;

  function formatDate(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: '2-digit' })
      + ' ' + d.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' });
  }

  function closeActivePopup() {
    if (activePopup) {
      activePopup.remove();
      activePopup = null;
    }
  }

  function renderPopup(p, idx) {
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
    if (existing.length === 0) {
      list.innerHTML = '<p class="comment-empty">Noch keine Anmerkungen.</p>';
    } else {
      existing.forEach(c => {
        const item = document.createElement('div');
        item.className = 'comment-item';
        item.innerHTML = `<div>${escHtml(c.text)}</div><div class="comment-item-meta">${formatDate(c.created_at)}</div>`;
        list.appendChild(item);
      });
    }
    popup.appendChild(list);

    const textarea = document.createElement('textarea');
    textarea.className = 'comment-textarea';
    textarea.placeholder = 'Anmerkung …';
    popup.appendChild(textarea);

    const submitBtn = document.createElement('button');
    submitBtn.className = 'comment-submit';
    submitBtn.textContent = 'Anmerken';
    submitBtn.onclick = async () => {
      const text = textarea.value.trim();
      if (!text) return;
      submitBtn.disabled = true;
      submitBtn.textContent = '…';
      const absatzText = p.textContent.slice(0, 120);
      const modus = showEntwurf ? 'entwurf' : 'final';
      try {
        const r = await fetch(COMMENT_API, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ kapitel_id: kapId, modus, absatz_idx: idx, absatz_text: absatzText, text }),
        });
        if (!r.ok) throw new Error('Fehler ' + r.status);
        if (!commentsByIdx[idx]) commentsByIdx[idx] = [];
        commentsByIdx[idx].push({ text, created_at: new Date().toISOString() });
        p.classList.add('has-comments');
        closeActivePopup();
        renderPopup(p, idx); // Popup neu öffnen mit neuem Kommentar
      } catch (e) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Fehler – nochmal versuchen';
      }
    };
    popup.appendChild(submitBtn);

    p.insertAdjacentElement('afterend', popup);
    activePopup = popup;
    textarea.focus();
  }

  function initComments(container) {
    const modus = showEntwurf ? 'entwurf' : 'final';
    fetch(`${COMMENT_API}?kapitel=${kapId}&modus=${modus}`)
      .then(r => r.json())
      .then(comments => {
        comments.forEach(c => {
          if (!commentsByIdx[c.absatz_idx]) commentsByIdx[c.absatz_idx] = [];
          commentsByIdx[c.absatz_idx].push(c);
        });

        const paras = container.querySelectorAll('p');
        paras.forEach((p, idx) => {
          // Trigger-Button
          const btn = document.createElement('button');
          btn.className = 'comment-trigger';
          btn.title = 'Anmerkung hinzufügen';
          btn.textContent = '✎';
          btn.onclick = (e) => {
            e.stopPropagation();
            if (activePopup && activePopup.dataset.idx == idx) {
              closeActivePopup();
            } else {
              renderPopup(p, idx);
            }
          };
          p.appendChild(btn);

          if (commentsByIdx[idx] && commentsByIdx[idx].length > 0) {
            p.classList.add('has-comments');
          }
        });

        // Klick außerhalb schließt Popup
        document.addEventListener('click', (e) => {
          if (activePopup && !activePopup.contains(e.target)) {
            closeActivePopup();
          }
        });
      })
      .catch(() => { /* silent fail — Kommentare laden nicht-kritisch */ });
  }

  // initComments aufrufen nachdem Kapitel geladen wurde
  // Wir patchen den bestehenden fetch-Callback
  const _origFetch = window._commentInitPending = true;
  document.addEventListener('chapter-rendered', (e) => {
    initComments(e.detail.container);
  });
}
```

- [ ] **Schritt 3: `chapter-rendered` Event dispatchen**

Im bestehenden `.then(md => { ... })` Block (nach `container.innerHTML = ...`), direkt nach der Zuweisung einfügen:

```javascript
if (isWip) {
  container.dispatchEvent(new CustomEvent('chapter-rendered', {
    bubbles: true,
    detail: { container }
  }));
}
```

- [ ] **Schritt 4: Lokal testen**

Seite `lesen/17/index.html` im Browser mit `?wip&entwurf` öffnen.  
Erwartung: Hover über Absatz zeigt `✎`-Button, Click öffnet Popup.

- [ ] **Schritt 5: Committen und deployen**

```bash
git add lesen/_reader.html
git commit -m "feat: Kommentarsystem — per-Absatz WIP-Anmerkungen"
git push
```

Deploy-Hook läuft automatisch.

---

## Selbst-Review Checklist

- [x] FastAPI validiert alle Inputs (Länge, erlaubte Werte)
- [x] CORS nur für alphina.net
- [x] SQLite-Datei liegt in gemountet-em Volume (persistent)
- [x] UI nur im `?wip`-Modus aktiv
- [x] `modus` wird aus URL-Params abgeleitet (entwurf vs final)
- [x] `kapitel_id` kommt aus dem bestehenden `kapId`-Wert
- [x] Kein XSS: `escHtml()` beim Rendern bestehender Kommentare (Funktion existiert in `_reader.html`)
- [x] Container im `caddy_default`-Netzwerk → Caddy kann `alphina-comments:8000` erreichen
