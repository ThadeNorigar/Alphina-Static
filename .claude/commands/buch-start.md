# /buch-start — Session starten

Starte eine neue Arbeitssession am Buchprojekt "Der Riss".

## Ablauf

### 1. Kontext laden

Lies folgende Dateien und fasse den aktuellen Stand zusammen:

- `state/current.md` — Letzter Stand
- `sessions/` — Letzte Session-Datei (neueste nach Datum)
- `buch/status.json` — Kapitel-Übersicht (wie viele pro Status, Gesamtwörter)

### 2. Offene Threads prüfen

Aus der letzten Session: Was ist offen? Was war der nächste Schritt?

### 3. Handoff-Check

Prüfe ob unterbrochene Pipeline-Phasen existieren:
```bash
ls buch/kapitel/*-handoff.md 2>/dev/null
```
Falls Handoff-Files gefunden: prominent anzeigen — diese Kapitel stecken MITTEN in der Pipeline und sollten als erstes weitergeführt werden. Zeige Phase und nächsten Command.

### 4. Werkzeuge prüfen

Falls der Moragh-Karten-Editor benötigt wird:
```bash
python moragh-server.py
```
→ http://localhost:8090

### 5. Ausgabe

```markdown
### Der Riss — Session Start

**Letzter Stand:** {1-2 Sätze aus state/current.md}

**Kapitel-Status:**
| Status | Anzahl | Wörter |
|--------|--------|--------|
| final  | N      | N      |
| lektorat | N   | N      |
| ausarbeitung | N | N    |
| entwurf-ok | N | N      |
| entwurf | N    | N      |
| szenenplan | N | N      |
| idee   | N      | N      |

(Nur Zeilen mit Anzahl > 0 anzeigen.)

**Unterbrochene Pipelines:**
- ⚠ `B1-K{KK}` — Handoff für Phase {X} liegt vor → nächster Schritt: `/{command} B1-K{KK}`
(Nur anzeigen wenn Handoff-Files existieren. Sonst weglassen.)

**Offene Threads:**
- [ ] Thread 1
- [ ] Thread 2

**Vorgeschlagener Fokus:** {Was als nächstes sinnvoll wäre}
```

### 6. Auf Autor warten

NICHT sofort losarbeiten. Frage: "Womit sollen wir starten?"

$ARGUMENTS
