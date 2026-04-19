# /brainstorm — Exploration ohne Canon-Commitment

Sandbox für Ideen, die *nicht* in den Canon wandern sollen. Plot-Alternativen, Was-wäre-wenn, Figuren-Was-wenn, Szenen-Varianten. Im Gegensatz zu `/entwurf` wird **nichts** in `buch/` geschrieben, **kein** Status geändert, **keine** Kaskade ausgelöst.

**Modell-Soll:** Sonnet (Plot-Arbeit, keine Prosa). Opus ist für diese Phase Verschwendung.

## Input

`$ARGUMENTS` = freier Topic-Text. Beispiele:
- `Was wäre wenn Alphina statt Sorel zuerst Maren trifft`
- `B1-K15 — Alternative Portal-Szene`
- `Vesper-Maren Dom-Wechsel temporär`

Wenn leer: fragen.

## Phase 0: Modell-Check

Wenn Session auf Opus läuft:

> WARNUNG: Brainstorm auf Opus zahlt 5x Aufpreis ohne Mehrwert. Plot-Arbeit ist Sonnet. Trotzdem weiter? [Autor antwortet]

Bei Sonnet/Haiku: stillschweigend weiter.

## Kernprinzip: Source-Tagging

**Default: untagged = der Autor hat es gesagt.** Das ist der Normalfall.

Drei Tags für Sonderfälle:

- **`<AI>...</AI>`** — KI-Vorschläge und Möglichkeiten. Nutze wenn du Ideen anbietest die der Autor nicht genannt hat. Kurz halten: 2-3 Optionen, keine Listen-Orgien.
- **`<hidden>...</hidden>`** — Autor-only Info für spätere Reveals. Geheime Motive, künftige Twists, Hintergrund den Figuren und Leserinnen nicht kennen.
- **`<rejected>...</rejected>`** — Ideen explizit verworfen. Mit Grund. Verhindert Re-Suggestion, erhält die Reasoning für späteres Wiederaufgreifen.

## Modi

### Interactive (Default)

Hin-und-her mit dem Autor. Fange Ideen ein wie sie entstehen, biete Möglichkeiten an wo hilfreich, stelle Fragen die Exploration vorantreiben.

Nach initialem Capture:
- Frage nach vagen Stellen, aber ohne sie aufzulösen
- Biete 2-3 Richtungen wenn Autor stockt
- Weise auf Implikationen hin, Verbindungen zu bestehenden Story-Threads
- Entwickle mit — übernimm nicht.

### Autonomous (für Fan-Out)

Ein scoped Prompt → strukturierter Brainstorm-Report. Für Multi-Angle-Exploration via mehreren parallelen Subagenten.

Im Autonomous-Modus:
- Alles mit `<AI>` taggen (nichts kam vom Autor)
- Optionen + Tradeoffs präsentieren, keine Empfehlungen
- Offene Fragen listen die Autor klären muss
- Scannable halten für Orchestrator-Synthese

Report-Struktur:

```markdown
# [Topic] — [Angle]

## Approach
Welchen Angle exploriert, warum.

## Ideas
<AI>Konkrete Möglichkeiten, logisch geordnet.</AI>

## Tradeoffs
<AI>Was jede Option gewinnt und aufgibt.</AI>

## Connections
<AI>Wie es zu existierenden Story-Threads passt/bricht.</AI>

## Open Questions
Fragen die der Autor vor Canon-Commit klären muss.
```

## Alphina-Guardrails (hart)

1. **Niemals** in `buch/*.md` schreiben. Nicht Storyline, nicht Aktpläne, nicht Szenenpläne, nicht Kapitel.
2. **Niemals** `status.json` oder `zeitleiste.json` modifizieren.
3. **Niemals** Kaskade auslösen (10-Ebenen-Hierarchie bleibt unberührt).
4. Output-Pfad: `story-in-work/brainstorm/brainstorm-{topic-slug}.md` — erstelle Ordner falls nicht vorhanden.
5. Wenn Autor nach Brainstorm entscheidet "das will ich canonisieren": **explizit** sagen "Das erfordert `/entwurf` oder manuelles Update in `buch/`. Hier im Brainstorm passiert nichts."

## Cross-POV-Awareness

Wenn Topic POV-spezifisch ist (Alphina, Sorel, Vesper, Maren):
- POV-Name im Dateinamen: `brainstorm-alphina-portal-alternative.md`
- Wenn Wortwahl diskutiert: Cross-POV-Regel erinnern (jeder POV eigene Wörter, siehe CLAUDE.md)
- Wenn Zweifel/Emotion diskutiert: Sorel-Prinzip erinnern (Premature Doubt verboten)

## Minimal Capture

Halte fest **was der Autor gesagt hat**. Keine Ausschmückung, keine Lücken füllen, keine Details erfinden die nicht erwähnt wurden.

**Das Problem ist Vermischung, nicht Vorschlagen.** KI-Vorschläge sind wertvoll — aber `<AI>`-getagged und kurz.

- "Sorel könnte vorher fliehen" → wie gesagt erfassen. Optional: `<AI>Nachts? Nach Maren-Gespräch? Durch Portal?</AI>`
- "Vielleicht Spannung" → als unsicher erfassen. Das "vielleicht" nicht auflösen.
- "Drei Fraktionen" → drei Fraktionen notieren. Nicht benennen.

## Vagheit bewahren

Wenn der Autor vage war, bleiben die Notizen vage. "Vielleicht", "eventuell", "sowas wie", "denke drüber nach" — alle erhalten.

Widersprüchliche Optionen **koexistieren** bis der Autor wählt. Nicht auflösen. Nicht "beste" wählen.

## Wenn du über-elaborierst — STOP

Stopp wenn du schreibst:
- Nummerierte Szenenlisten die der Autor nicht beschrieb
- Detaillierte Backstories aus einer einzigen Eigenschaft
- Konkrete Dialoge die niemand anforderte
- Mehrere Absätze pro Bullet
- Beispiele die der Autor nicht gab

Erfolgs-Test: Der Autor sagt "ja, genau das habe ich gesagt" — nicht "das habe ich nie alles gesagt."

## Ablauf

1. Erstelle `story-in-work/brainstorm/` wenn nicht vorhanden
2. Topic-Slug aus `$ARGUMENTS` generieren (lowercase, bindestrich-getrennt, max 50 Zeichen)
3. Datei: `story-in-work/brainstorm/brainstorm-{slug}.md`
4. Header: `# Brainstorm: {Topic}` + `*{Datum} · Status: explorativ, nicht Canon*`
5. Bei Interactive: Konversation führen, nach jeder Runde File updaten
6. Bei Autonomous: Report-Struktur einmal schreiben, fertig
7. **Kein git add, kein commit, kein deploy.** Autor entscheidet selbst ob er brainstorm-Files committen will.

## Reminder am Ende

Nach dem Brainstorm dem Autor zeigen:

> Brainstorm gespeichert: `story-in-work/brainstorm/brainstorm-{slug}.md`
>
> **Nicht im Canon.** Für Canon-Commit: `/entwurf` oder manuelles Update in `buch/`. Brainstorm-Files kannst du behalten, löschen, oder später als Referenz für echte Arbeit ziehen.

$ARGUMENTS
