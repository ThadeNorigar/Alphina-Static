# /lektorat-online — Online-Kommentare abarbeiten und als erledigt markieren

Interaktive Pipeline: holt offene Kommentare ab, geht sie einzeln mit dem Autor durch, wendet Edits an, committet, markiert die Kommentare in der DB als erledigt.

**Modell-Soll:** Sonnet (Default). Opus nur wenn Inhalt-Fixes bevorstehen.

## Nutzung

- `/lektorat-online B1-K17` — Alle offenen Kommentare zu K17 durchgehen (final + lektorat)
- `/lektorat-online B1-K17 heute` — Nur heute eingegangene offene Kommentare
- `/lektorat-online B1-K17 seit 2026-04-13` — Ab Datum
- `/lektorat-online B1-K17 final` — Nur final-Modus

## Was der Skill tut

### 1. Guard-Checks

- `buch/kapitel/{ID}-handoff.md` existiert nicht erforderlich (im Lektorat kein Handoff noetig)
- Status aus `buch/status.json` pruefen: muss `lektorat` oder `final` sein
- Wenn `final`: Warnung, dass Aenderungen Zurueckstufung bedeuten

### 2. Kommentare holen

```bash
curl -s "https://alphina.net/api/comments?kapitel={slug}&modus=final" \
  -H "X-User-Id: 21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e"
curl -s "https://alphina.net/api/comments?kapitel={slug}&modus=lektorat" \
  -H "X-User-Id: 21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e"
```

Default: nur offene (`resolved_at IS NULL`) — das API-Default ohne `include_resolved=true`.

Bei Datums-Filter: Ergebnisse nach `created_at` filtern (clientseitig, ISO-String-Vergleich).

### 3. Kapiteldatei laden

`buch/kapitel/{datei aus status.json}` — das ist der Text der gerade online steht.

Falls Fakten-Frage auftaucht: `python scripts/kapitel-kontext.py {ID} --phase lektorat` verwenden.

### 4. Pro Kommentar: Durchgehen

Fuer jeden offenen Kommentar — in sortierter Reihenfolge (absatz_idx, created_at):

1. Kommentar zeigen: ID, Absatz, Zitat (absatz_text), Kommentar-Text
2. Vorschlag formulieren: Edit-Vorschlag in Prosa, Grund
3. Auf Autor-Antwort warten: `ja` / `nein` / `anders` / `skip` / `wontfix` / `reopen`
4. Entscheidung umsetzen:
   - **ja** → Edit-Tool anwenden, Kommentar als `done` markieren (nach Commit)
   - **nein / wontfix** → Kommentar als `wontfix` markieren mit Begruendung in `note`
   - **anders** → Autor liefert alternative Formulierung, Edit danach, dann `done`
   - **skip** → ueberspringen, Kommentar bleibt offen (fuer spaeter)
   - **reopen** → nur bei bereits resolved; setzt zurueck

Keine Kommentare im Batch gleichzeitig abarbeiten — immer einzeln bestaetigen.

### 5. Commit pro Durchgang

Wenn alle offenen Kommentare durch sind (oder Autor sagt Stop):

```bash
git add buch/kapitel/{datei}
git commit -m "fix({ID}): Lektorat — Anmerkungen {datum/bereich} eingearbeitet

- Komm #{id1}: {kurze beschreibung}
- Komm #{id2}: {kurze beschreibung}
- ...
"
git push
# Deploy laeuft per Hook
```

### 6. Kommentare als erledigt markieren

Nach erfolgreichem Push: fuer jeden abgearbeiteten Kommentar:

```bash
curl -s -X PATCH "https://alphina.net/api/comments/{id}" \
  -H "X-User-Id: 21c7ef896af35a6ce31b79c1f712b94a4f1d523b911de20e" \
  -H "Content-Type: application/json" \
  -d '{"status":"done","commit":"{commit-hash}","note":"{kurze beschreibung}"}'
```

Status-Werte:
- `done` — umgesetzt, mit commit-Hash
- `wontfix` — bewusst nicht umgesetzt, mit note
- `rejected` — Kommentar trifft nicht zu (z.B. Canon-Widerspruch beim Leser)
- `reopen` — nur fuer Debugging: zuruecksetzen auf offen

### 7. Abschluss-Bericht

Am Ende:
- Wie viele `done` / `wontfix` / `skip`
- Commit-Hash
- Hinweis: Seite neu laden zeigt erledigte Kommentare ausgeblendet

## Regeln

- Edit-Tool > Write-Tool
- Nichts anfassen was der Autor nicht angefragt hat
- Status `final` NUR auf explizites OK
- Deutsch, Umlaute ausschreiben
- Nie Kommentare mehrerer Tage/Autoren ohne Autor-Bestaetigung vermischen
- Wenn Kommentar als Frage kommt ("kann er das ueberhaupt beurteilen?"): als Rueckfrage an Autor weitergeben, nicht eigenmaechtig fixen

## Bekannter Comment-Status (Kontext)

Die DB-Schema hat folgende resolved_*-Felder:
- `resolved_at` — ISO-Datum oder NULL
- `resolved_status` — `done` | `wontfix` | `rejected`
- `resolved_commit` — Git-Hash
- `resolved_note` — kurze Beschreibung

GET-Default liefert nur offene. Mit `?include_resolved=true` gibt's alle.

$ARGUMENTS
