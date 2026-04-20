# Handoff — B1-K23 (Ausarbeitung → Lektorat)

**Von Phase:** ausarbeitung → **Zu Phase:** lektorat
**Erstellt:** 2026-04-20
**Status beim Handoff:** lektorat

## Modell-Empfehlung

`claude --model sonnet` (oder Haiku für Feinschliff, Token-sparend)

## Aufruf für nächste Session

`/lektorat-fix B1-K23`

## Kontext

- **POV:** Alphina (3. Person nah / Präteritum)
- **Umfang:** 2.059 Wörter (Ziel war 2.500 — bewusst kompakt gehalten, Handoff-Vorgabe)
- **Timeline:** 22. Blütenmond 551, Abend. Selber Tag wie K22 morgens.
- **Ort:** Alphinas Zimmer im *Anker*, erste Etage, Hafengasse
- **Finale Datei:** `buch/kapitel/B1-K23-alphina.md`

## Was in der Ausarbeitung passiert ist

### Drei Checks bestanden
- **Logik-Check:** 4 Findings eingearbeitet (Henriks Hinterhof geklärt, Werkzeugdose-Untersetzer → Zinnschale, Lichthaus-Farne vor drei Wochen → Messungen am Steinkreis, "zwei plus drei" → "Summe der Einzeltests")
- **Stil-Check:** 6 Findings eingearbeitet (Antithesen 8→1, Geschmack in Nähe-Szene ergänzt, Anapher aufgelöst, Stakkato-Inflation entspannt, Kontrollverlust-Moment eingebaut, Alphinas Begehren-Register aktiviert)
- **Council (Fiction, 4 Rollen):** 7 Findings eingearbeitet (Fenster-Widerspruch, Register-Bruch "Größenordnungen", Metaphern-Stau entzerrt, Geschmack-Timing, Kerzen-Übergang, Fragment-Feuer nach Klimax, Sub-Markierung Sorel — später korrigiert, siehe unten)

### Nachträgliche Autor-Korrekturen
- **Henrik-Kanon:** Henrik ist Gärtner im Botanischen Garten in Vael, nicht in Velde. Steckling ist "aus dem Botanischen Garten, von Henrik".
- **Kein Salz/Metall auf Lippen:** Reflex-Pattern entfernt, durch Pyrogallol-Dunst im Gaumen ersetzt (später Material-Dichte weiter reduziert).
- **Alphina/Sorel ≠ BDSM:** Sub-Gesten für Sorel (offene Handflächen, Kopf gesenkt, Blick bietet) wurden entfernt; ersetzt durch "Er wartete. Die Hände lagen ruhig auf den Oberschenkeln. Er hielt den Blick, aber er drückte nichts hinein." — Charakter, keine Rolle.
- **Materialdichte reduziert:** Pyrogallol 3× → 1× (nur Einführung bleibt). Neue Memory-Regel: Chemikalien max 1-2× pro Kapitel.

### Ausgebaute Stellen (Block-Workflow, +150 W)
- Nach K19-Rekonstruktion: Zwei-Atemzüge-Stille mit Kerze, Schritten in der Gasse, Blick auf Sorels Hand
- Zwischen Einzeltests: Nähe-ohne-Berührung körperlich ausgearbeitet (Wärme-Radius, gemeinsames Atmen, Gewicht zwischen den Händen)
- Aftermath nach Kuss, vor Aufstehen: Schulter/Stirn/Atem, Dämmerung kriecht die Fassaden hoch

## Was das Lektorat prüfen sollte

- **Feinkorrekturen Satzrhythmus:** KURZ 61% / MITTEL 28% / LANG 11% — Mittelbau sollte Rest noch weiter hochkommen.
- **Stakkato-Dichte:** einzelne Fragment-Ketten verbleiben ("Sie saßen. Keiner stand auf."; "Nickte. Einmal.") — im Zweifel behalten, sind Alphina-Signatur.
- **Berufslinse-Dichte:** Auxine-Passage Z.61 und Ranken-Beschreibungen — insgesamt ca. 10-12%, knapp über dem neuen 10%-Limit. Ggf. eine botanische Erklärung weiter verknappen.
- **Typos / Umlaute / Interpunktion:** Standard-Feinschliff.
- **Genus-Konsistenz:** "die Schale" mehrfach umgestellt, nochmal prüfen.
- **Monatsnamen:** Blütenmond nicht Mai — ist konsistent.
- **Du-Anrede Alphina/Sorel:** seit K21 durchgezogen — konsistent.

## Offene Punkte (eventuell im Lektorat schließen oder ignorieren)

- Wortziel 2500 W vs. aktuell 2059 W — bewusst kompakt, Handoff-Erlaubnis. Falls im Lektorat Stellen auffallen, die noch Atemraum brauchen, dort vorsichtig ausbauen (Block-Workflow: 100 W + Self-Check).
- "Keine Chemikalien im Gaumen-Geschmack mehr" — Z.115 "Keller-Dunst, bitter, trocken" steht so; falls zu abstrakt, konkretisieren ohne Chemikalien-Namen.

## Memory-Regeln dieser Session (für Nachfolgekapitel)

- Kein Salz/Metall-Reflex auf Lippen (`feedback_kein_salz_metall_lippen.md`)
- Berufslinse max 10% (`feedback_berufslinse_max_10_prozent.md`)
- Alphina/Sorel = kein BDSM (`project_alphina_sorel_kein_bdsm.md`)
- Materialdichte niedriger, Chemikalien max 1-2× (`feedback_materialdichte_reduzieren.md`)
- Ausarbeitung blockweise 100-150 W + Self-Check (`feedback_ausarbeitung_blockweise.md`)

## Nächste Phase nach Lektorat

Status: lektorat → final
Dann: Commit + Deploy (automatisch via Git-Hook)
