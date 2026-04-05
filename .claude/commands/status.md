# /status — Kapitel-Status aktualisieren

Verwalte den Status der Kapitel in `buch/status.json`.

## Nutzung

- `/status` — Zeigt aktuellen Status aller Kapitel
- `/status 02 entwurf` — Setzt Kapitel 02 auf "entwurf"
- `/status 02 final 4013` — Setzt Kapitel 02 auf "final" mit 4013 Wörtern
- `/status I1 lektorat` — Setzt Interludium I auf "lektorat"

## Gültige Stati (in Reihenfolge)

1. **idee** — Nur die Idee existiert
2. **szenenplan** — Szenen-Definition geschrieben (buch/szenen/XX-NN.md)
3. **entwurf** — Erster Text geschrieben (buch/kapitel/XX-*.md)
4. **council** — Council-Review durchlaufen
5. **logik-check** — /logik-check bestanden
6. **lektorat** — Stilistisch überarbeitet
7. **final** — Fertig

## Was der Skill tut

1. Lies `buch/status.json`
2. Wenn keine Argumente: zeige Zusammenfassung (wie viele pro Status, Gesamtwörter)
3. Wenn Argumente: aktualisiere den Status des angegebenen Kapitels
4. Schreibe `buch/status.json` zurück
5. Zeige den aktualisierten Eintrag

## Regeln

- Status darf nur VORWÄRTS gehen (idee → szenenplan → entwurf → ...) oder auf "idee" zurückgesetzt werden
- Bei "final": Wortanzahl ist Pflicht (zähle mit `wc -w` wenn nicht angegeben)
- Warnung wenn ein Kapitel auf "final" gesetzt wird ohne dass /logik-check gelaufen ist

$ARGUMENTS
