# /status — Kapitel-Status aktualisieren

Verwalte den Status der Kapitel in `buch/status.json`.

## Nutzung

- `/status` — Zeigt aktuellen Status aller Kapitel
- `/status 02 entwurf` — Setzt Kapitel 02 auf "entwurf"
- `/status 02 final 4013` — Setzt Kapitel 02 auf "final" mit 4013 Wörtern
- `/status I1 lektorat` — Setzt Interludium I auf "lektorat"

## Gültige Stati (in Reihenfolge)

1. **idee** — Nur die Idee existiert
2. **entwurf** — Plot-Entwurf geschrieben (`buch/kapitel/B1-K{NN}-entwurf.md`, Phase `/entwurf`)
3. **entwurf-checked** — Entwurf auf Canon/Logik geprüft
4. **entwurf-ok** — Entwurf Autor-freigegeben für Ausarbeitung
5. **ausarbeitung** — Prosa geschrieben (`/ausarbeitung`)
6. **lektorat** — In Lektorat (`/lektorat-fix`)
7. **final** — Fertig

**Legacy-Stati** (nur noch auf Altbestand zulässig, nicht für neue Kapitel): `szenenplan`, `council`, `logik-check`, `stil-check`, `final-council`. Die Status-Stufe `szenenplan` ist obsolet — Szenenpläne wurden am 22. Apr 2026 nach `buch/szenen/_archiv_2026-04-22/` verschoben. Neue Kapitel gehen direkt `idee → entwurf`.

## Was der Skill tut

1. Lies `buch/status.json`
2. Wenn keine Argumente: zeige Zusammenfassung (wie viele pro Status, Gesamtwörter)
3. Wenn Argumente: aktualisiere den Status des angegebenen Kapitels
4. Schreibe `buch/status.json` zurück
5. Zeige den aktualisierten Eintrag

## Regeln

- Status darf nur VORWÄRTS gehen (idee → entwurf → entwurf-checked → entwurf-ok → ausarbeitung → lektorat → final) oder auf "idee" zurückgesetzt werden
- Bei "final": Wortanzahl ist Pflicht (zähle mit `wc -w` wenn nicht angegeben)
- Warnung wenn ein Kapitel auf "final" gesetzt wird ohne dass /logik-check UND /stil-check gelaufen sind
- Warnung wenn ein Gate-Status übersprungen wird (z.B. direkt von council auf final)

$ARGUMENTS
