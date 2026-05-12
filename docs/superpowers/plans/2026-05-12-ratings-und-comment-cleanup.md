# Szenen-Ratings + Kommentar-Cleanup (2026-05-12)

**Ziel:** Frontend für Szenen-Ratings ist eingebaut (`lesen/_reader.html`) und
das Diff-Feature ist entfernt. Damit das Rating speichern und lesen kann,
braucht der FastAPI-Server `/home/adrian/apps/alphina-comments/server.py`
zwei neue Endpoints. Außerdem soll die alte `comments`-Tabelle nach Archivierung
geleert werden.

## Stand Frontend

- `lesen/_reader.html` ruft beim Lesen jeder Szene `POST /api/ratings`
  mit `{ kapitel_id, modus, szene_idx, rating }` auf und `GET /api/ratings?kapitel=…&modus=…`
  beim Laden des Kapitels. Header: `X-User-Id` wie bei Kommentaren.
- Das Diff-Feature ist komplett aus `_reader.html` entfernt — der Endpoint
  unter `/story-in-work/lektorat-versions/` wird nicht mehr geladen, kann
  bleiben oder später entfernt werden.
- Backup-Skript `scripts/archive-comments.py` zieht alle Kommentare
  (`include_resolved=true`) und schreibt sie nach
  `buch/_archiv/online-kommentare-YYYY-MM-DD.{json,md}`.

## Task 1 — Ratings-Tabelle + Endpoints

**Files (Server, via SSH):**

- Ändern: `/home/adrian/apps/alphina-comments/server.py`

### Schritt 1: Schema erweitern

```python
def init_db():
    with get_db() as conn:
        # … existing comments-Tabelle …
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT    NOT NULL,
                kapitel_id  TEXT    NOT NULL,
                modus       TEXT    NOT NULL DEFAULT 'final',
                szene_idx   INTEGER NOT NULL,
                rating      INTEGER NOT NULL,
                updated_at  TEXT    NOT NULL,
                UNIQUE (user_id, kapitel_id, modus, szene_idx)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ratings_kapitel ON ratings(kapitel_id, modus)")
        conn.commit()
```

Ein Eintrag pro `(user, kapitel, modus, szene)`. UPSERT überschreibt das
bisherige Rating.

### Schritt 2: Pydantic-Modelle

```python
class RatingIn(BaseModel):
    kapitel_id: str
    modus: str
    szene_idx: int
    rating: int

    @field_validator("kapitel_id")
    @classmethod
    def validate_kapitel(cls, v: str) -> str:
        if not v or len(v) > 10:
            raise ValueError("kapitel_id ungueltig")
        return v

    @field_validator("modus")
    @classmethod
    def validate_modus(cls, v: str) -> str:
        if v not in ("entwurf", "final"):
            raise ValueError("modus muss 'entwurf' oder 'final' sein")
        return v

    @field_validator("szene_idx")
    @classmethod
    def validate_szene(cls, v: int) -> int:
        if v < 0 or v > 100:
            raise ValueError("szene_idx ausserhalb 0..100")
        return v

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: int) -> int:
        if v < 1 or v > 5:
            raise ValueError("rating muss 1..5 sein")
        return v
```

### Schritt 3: Endpoints

```python
@app.get("/api/ratings")
def get_ratings(kapitel: str, modus: str = "final", x_user_id: str | None = Header(None)):
    if not x_user_id:
        raise HTTPException(401, "X-User-Id Header fehlt")
    # Admin-Key (gleicher wie comments): liefert alle User aggregiert
    is_admin = x_user_id == os.environ.get("ADMIN_KEY", "")
    with get_db() as conn:
        if is_admin:
            rows = conn.execute(
                "SELECT user_id, szene_idx, rating, updated_at FROM ratings "
                "WHERE kapitel_id = ? AND modus = ? ORDER BY szene_idx, updated_at",
                (kapitel, modus),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT szene_idx, rating, updated_at FROM ratings "
                "WHERE user_id = ? AND kapitel_id = ? AND modus = ? "
                "ORDER BY szene_idx",
                (x_user_id, kapitel, modus),
            ).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/ratings", status_code=201)
def post_rating(body: RatingIn, x_user_id: str | None = Header(None)):
    if not x_user_id:
        raise HTTPException(401, "X-User-Id Header fehlt")
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO ratings (user_id, kapitel_id, modus, szene_idx, rating, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (user_id, kapitel_id, modus, szene_idx)
            DO UPDATE SET rating = excluded.rating, updated_at = excluded.updated_at
            """,
            (x_user_id, body.kapitel_id, body.modus, body.szene_idx, body.rating, now),
        )
        conn.commit()
    return {"ok": True, "rating": body.rating}
```

### Schritt 4: Aggregation für die Autor-Sicht (optional, nächste Iteration)

Ein zweiter Admin-Endpoint kann später Durchschnitte pro Szene/Kapitel liefern,
z.B. `/api/ratings/aggregate?kapitel=17`. Erstmal reicht der Roh-Dump.

### Schritt 5: Deploy

```bash
ssh adrian@adrianphilipp.de "cd ~/apps/alphina-comments && docker compose restart"
```

## Task 2 — Kommentare archivieren + DB leeren

1. **Backup lokal:** vor allem anderen
   ```bash
   python scripts/archive-comments.py
   git add buch/_archiv/online-kommentare-*.{json,md}
   git commit -m "archiv: Online-Kommentare Snapshot YYYY-MM-DD"
   ```

2. **DB leeren** (auf Server, nach erfolgreichem Commit des Backups):
   ```bash
   ssh adrian@adrianphilipp.de "sqlite3 /var/lib/docker/volumes/alphina-comments_data/_data/comments.db 'DELETE FROM comments;'"
   ```
   Pfad zum Volume ggf. anpassen — `docker volume inspect alphina-comments_data` gibt den Mountpoint.

   Alternativ: `DELETE`-Endpoint auf den Server, der mit Admin-Key alle Kommentare löscht. Weniger ad-hoc, aber für eine einmalige Aktion overkill.

3. **Verifikation:**
   ```bash
   curl -s "https://alphina.net/api/comments?kapitel=17&modus=final&include_resolved=true" \
     -H "X-User-Id: 21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e"
   ```
   Erwartet: `[]`.

## Skill-Anpassungen (Folge-Arbeit)

- `.claude/commands/lektorat-online.md` und `.claude/commands/kommentare.md`
  bleiben funktional — sie sprechen die `comments`-API an, die mit leerer Tabelle
  einfach `[]` liefert. Wenn das Kommentar-Feature dauerhaft raus soll, beide
  Skills entfernen.
- Neuer Skill `/ratings`: holt aggregierte Sterne pro Szene mit Admin-Key.
  Noch offen, kommt erst, wenn Daten reinkommen.
