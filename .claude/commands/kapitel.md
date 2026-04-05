# /kapitel — Nächstes Kapitel schreiben

Du schreibst das nächste Kapitel von "Der Riss".

## Phase 0: Kontext laden

1. Lies `buch/02-akt1.md` — welches Kapitel ist dran?
2. Lies `buch/00-welt.md` — Welt, Figuren, Magie
3. Lies `buch/02-stilregeln-v2.md` — Stilregeln
4. Lies das letzte fertige Kapitel in `buch/kapitel/` — für Ton und Konsistenz
5. Prüfe: Welche Tschechow-Waffen sind geladen? Was muss aufgegriffen werden?

## Phase 1: Szenenplan

Erstelle `buch/kapitel/XX-entwurf.md` mit:
- POV-Figur und Perspektive (Ich/Präsens für Alphina, 3.Person/Präteritum für andere)
- 2-4 Szenen mit Beats
- Tschechow-Waffen die geladen werden
- Referenzen zu früheren Kapiteln
- Wortziel pro Szene (~1.200-1.600), Gesamtziel: 4.000-4.500 Wörter

Dann: Council auf den Entwurf (`/council buch/kapitel/XX-entwurf.md`)

## Phase 2: Szene für Szene

**GATE: Keine nächste Szene ohne abgeschlossenen Council + Fixes der aktuellen.**

Für jede Szene, einzeln, der Reihe nach:
1. Schreibe die Szene in `buch/kapitel/XX-szeneN.md`
2. `wc -w` prüfen (Ziel: 1.200-1.600 pro Szene)
3. **Council auf diese Szene** — Erzähldichte, Logik, Stilmuster, Stilbudget-Zählung
4. Fixes einarbeiten
5. Erst dann: nächste Szene

## Phase 3: Zusammenbauen

1. Alle Szenen in `buch/kapitel/XX-FIGUR.md` zusammensetzen
2. `wc -w` Gesamtkapitel — **Minimum 4.000 Wörter.** Unter 4.000 → zurück und verdichten.
3. **Logik-Checkliste (manuell, jeden Punkt einzeln):**
   - Tageszeit? (konsistent über alle Szenen)
   - Wetter? (Jahreszeit, Temperatur)
   - Ort? (Figur verlässt nie den Raum ohne Grund)
   - Wissen der Figur? (weiß nur was sie wissen kann)
   - Puls/Körper? (nie Emotionen benannt, immer gezeigt)
   - Referenzen zu früheren Kapiteln?
   - Technologie? (frühes 19. Jhd, kein Strom)

## Phase 3.5: Logik-Check (GATE 1)

`/logik-check buch/kapitel/XX-FIGUR.md`

→ Bericht + Zusammenfassung + Verdikt
→ **Warte auf Freigabe durch Autor**
→ Fixes einarbeiten
→ **Warte auf Bestätigung der Fixes**

**GATE: Keine Phase 3.6 ohne explizite Autor-Freigabe.**

## Phase 3.6: Stil-Check (GATE 2)

`/stil-check buch/kapitel/XX-FIGUR.md`

→ Bericht + Zusammenfassung + Verdikt
→ **Warte auf Freigabe durch Autor**
→ Fixes einarbeiten
→ **Warte auf Bestätigung der Fixes**

**GATE: Keine Phase 3.7 ohne explizite Autor-Freigabe.**

## Phase 3.7: Final Council (GATE 3)

`/council buch/kapitel/XX-FIGUR.md`

→ 3-Agenten-Review + Verdikt
→ **Warte auf Freigabe durch Autor**

**GATE: Keine Phase 4 ohne explizite Autor-Freigabe.**

## Phase 4: Deploy

```bash
# Kapitel zusammenbauen, committen, deployen
git add -A && git commit -m "feat: Kapitel XX — [Figur], [Seitenzahl]S, [Wörter]W" && git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull"
```

## Regeln

- Lies IMMER das vorherige Kapitel vor dem Schreiben
- Jede Szene wird einzeln gecounciled
- Kein Kapitel ohne Logik-Check
- Wortzählung nach JEDER Szene
- Umlaute verwenden (ä, ö, ü, ß)

$ARGUMENTS
