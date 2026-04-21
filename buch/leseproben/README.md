# Leseproben — Ton-Etüden für alle Register

Dieser Ordner enthält **Ton-Referenz-Etüden** für jedes Register des Positionings (`buch/00-positioning.md`). Jede Probe ist ~400–600 Wörter, konkretisiert einen Stilvektor oder ein dunkles Register, und dient als Kalibrierungs-Beispiel für Skills wie `/entwurf`, `/ausarbeitung`, `/stil-check`, `/refit`, `/council`.

## Status: Ton-Etüden, nicht Plot-Canon

- Die Proben nutzen Haupt- und Nebenfiguren des Canons.
- Sie sind **nicht Teil des Plot-Kanons** — jederzeit überschreibbar, nicht bindend für Zeitleiste oder Figurenstand.
- Plot-Beats in einer Probe **widersprechen nicht dem Canon**, sind aber frei in der Szenen-Konstellation.
- Wenn eine Probe mit dem Canon kollidiert: die Probe wird angepasst, nicht der Canon.

## YAML-Header-Schema

```yaml
---
kategorie: <Banter / Heat / BDSM / Welt-warm / Krieg / ...>
pov: <Figurname>
figuren: <Liste>
register: <commercial Romantasy / BDSM / Dark Fantasy / Dunkles Register>
heat_level: <keine / leise / commercial / explizit non-BDSM / explizit BDSM / Drohung / Gewalt>
primaer_referenz: <Autorin + Werk>
ergaenzende_referenz: <Autorin + Werk, optional>
zweck: <Ton-Referenz für welche Szenen>
canon_status: Ton-Etüde, nicht Plot-Canon
---
```

## Liste

### B1-Commercial-Kern

| # | Kategorie | POV | Heat |
|---|-----------|-----|------|
| 01 | Banter / Slow-Burn-Tension | Alphina | leise |
| 02 | Kippmoment: erster Kuss / Fast-Kuss | Alphina | commercial |
| 03 | Heat Alphina/Sorel explizit | Alphina | explizit non-BDSM |
| 04 | BDSM-Power im Alltag | Maren | leise (Power-Exchange) |
| 05 | BDSM-Szene explizit | Maren | explizit BDSM |
| 06 | Aftercare-Miniatur | Vesper | ruhig (Care-Beat) |
| 07 | Antagonisten-Szene Varen | Alphina | Drohung |
| 08 | Magie-Kontrollverlust | Alphina | Action-Heat |
| 09 | Welt Vael warm (Werft) | Maren | keine |
| 10 | Welt Vael kalt (Archiv/Uhrwerk) | Vesper | keine |
| 11 | Moragh-Ankunft mit Gefahr | Alphina | Drohung |
| 12 | Gruppenszene mit verborgener Tension | wechselnd | leise unter der Oberfläche |

### B2/B3-Dunkle Register

| # | Kategorie | POV | Heat |
|---|-----------|-----|------|
| 13 | Krieg / Schlachtfeld | Alphina (B2) | Gewalt |
| 14 | Völkermord-Täter-POV (Quellen-Zerstörung) | Alphina (B2) | Gewalt |
| 15 | Post-Krieg-Ruine (tote Zone) | Alphina (B2) | Drohung |
| 16 | Biotech-Dystopie / Expedition 2 | Nyr (B3) | Gewalt |
| 17 | Körper-Mutilation / Amputation | Alphina (B3) | Gewalt |
| 18 | Fehlurteil-Schuld (nach Talven) | Alphina (B3) | Trauer |
| 19 | Narbige Ruhe / Epilog | Alphina (B3) | keine |

## Commercial-Mindeststandards (95%-Gate)

**Jede Probe muss das 95%-Gate aus `00-positioning.md` Abschnitt 9 passieren.** Leserinnen-Test verpflichtend via `/book-council` vor Commit. Die vier Pflichten:

1. Erster Satz ist Hook (Figur in Situation mit Spannung, nicht Atmosphäre)
2. Figur will etwas, deutlich
3. Etwas passiert/kippt in den ersten 200 Wörtern
4. Körper oder Emotion hörbar im ersten Viertel

**Pass-Stufen:**
- ≥ 90 % → bestanden
- 70–89 % → chirurgische Fixes
- < 70 % → Neuansatz

## Anwendung in Skills

- **`/book-council`**: **Pflicht-Check** für jede neue Probe. Fünf Ziel-Leserinnen-Archetypen (LINA/NORA/MEIKE/VICTORIA/KAYA) bewerten die Commercial-Marktfähigkeit.
- **`/entwurf`**: Probe zum Szenen-Typ laden als Ton-Referenz.
- **`/ausarbeitung`**: Primär-Probe + ggf. Ergänzungs-Probe laden. Ersetzt das "letzte fertige Kapitel derselben POV-Figur" nicht, sondern ergänzt.
- **`/stil-check`**: Findings gegen die Probe für den Szenen-Typ messen.
- **`/refit`**: Die Probe ist das Zielbild; altes Kapitel wird daran gemessen.
- **`/council`**: jeder Agent darf die Probe zitieren als Ton-Vergleich (Canon-Focus, nicht Markt-Focus).

## Was diese Proben NICHT sind

- Keine Vorlagen zum 1:1-Kopieren. **Ton-Richtung**, nicht Mimikry-Ziel.
- Keine Plot-Entscheidungen. Canon liegt in `00-welt.md`, `00-storyline.md`, `zeitleiste.json`.
- Keine Stil-Regeln. Regeln in `02-stilregeln-v2.md`.
- Keine Vollszenen. Eine Probe zeigt **einen Register-Zustand** in ~500 Wörtern, keine komplette Dramaturgie.
