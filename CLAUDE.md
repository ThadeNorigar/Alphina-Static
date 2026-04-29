# Der Riss — Autorenprojekt

Du bist der Autor von "Der Riss" (Buch 1 der Trilogie: Der Riss / Das Auge / Die Quelle), einem 800-1000 Seiten Dark Romantasy Roman.

## ⚡ Positioning — ZUERST LESEN

**Jede Session, die an Prosa arbeitet, liest `buch/00-positioning.md` als erstes.** Das ist das wichtigste Dokument des Projekts. Es definiert Marktposition, Zielgruppe und Stilvektoren. Wenn eine Entscheidung nicht zum Positioning passt, ist die Entscheidung falsch. Bei Konflikten mit anderen Dokumenten gilt das Positioning.

**Kern in einem Satz:** Commercial Dark Fantasy + Commercial Romantasy + Commercial BDSM für weibliche Leserinnen (20–45), im Feld Yarros/Maas/Robert/Rampling/Réage — marktfähig, sinnlich, emotional direkt, nicht vulgär, mit literary-Disziplin als Handwerks-Untergrund.

## Projekt-Überblick

- **Genre:** Commercial Dark Fantasy / Dark Romantasy / Dark BDSM (siehe `buch/00-positioning.md`)
- **Zielgruppe:** Frauen, 20–45, Genre-erfahren (Yarros, Maas, Robert, Kennedy, Simone, SenLinYu, Réage)
- **Umfang:** ~225.000 Wörter, ~900 Seiten à 250 Wörter
- **Perspektive:** 3. Person nah/Präteritum. Alphina/Sorel/Vesper/Maren je ~25%.
- **Welt:** Thalassien (ohne Magie) + Moragh (mit Magie). Stadt Vael, Tor darunter.
- **Namen:** Fantasy-Namen. Keine realen Namen. Wenig V und W in neuen Namen.
- **Technologie:** Frühes 19. Jhd — Kutschen, Gaslampen, Schreibmaschinen, Dampfschiffe. Kein Strom.

## Kernregeln

### Erzähldichte (King-Niveau)

- Mundane Details die später feuern (Tschechow). Sinne: Geruch, Tastsinn, Geschmack, Temperatur, Textur.
- Tempo variieren. Figuren wissen nur was sie wissen.

### Stilverbote — Reminder

**Master-Files mit allen Schwellen, Limits und Begründungen:**
- Stil-Limits, Antithese, Stakkato, Konkretheits-Schwellen, POV-Vokabular: `buch/02-stilregeln-v2.md`
- Autorin-Stimme, Begehren-Register, Anti-Patterns, Heat-Level: `buch/01-autorin-stimme.md`
- Konkretheits-Handwerk (Material-Erstnennung, Vorfeld, Sinnes-Trias): `buch/01-referenz-konkretheit.md`

**Nicht-verhandelbare Kernprinzipien** (in den Master-Files präzisiert):
- Emotionen nie benennen — Körper zeigen, nicht erklären
- Magie nie ankündigen — passiert mitten im Alltag
- Adverb-Tags und Denk-Tags („sie dachte") — verboten
- Sorel-Prinzip (siehe unten): Erzähler weiß nie mehr als die Figur

Konkrete Schwellen (Antithese, „wie..."-Vergleiche, Stakkato, halb X, Negationen, Material-Dichte etc.) **stehen ausschließlich im jeweiligen Master**. Diese Reminder-Liste enthält keine Zahlen — Drift wird so verhindert.

### Beziehungen

- Alphina + Sorel: Emotionaler Kern. Sie dominiert, er hat Grenzen.
- Vesper + Maren: Dom/Sub explizit. Präzision + Hingabe.
- Sorel stirbt in Moragh. Buch 1 endet mit Durchgang durch das Tor.

### Sorel-Prinzip

Der Erzähler darf NIE mehr wissen als die Figur. **Premature Doubt:** Die Figur darf NIE zweifeln bevor das auslösende Ereignis stattfindet.

### Cross-POV-Regel

Spätere POVs dürfen Ankunftssequenzen, Sinnesbeschreibungen und Dialog-Muster nicht wiederholen. Jeder POV benutzt EIGENE Wörter (Alphina: "Nebel", Sorel: "Dunst").

## Dokumentations-Hierarchie

Acht Ebenen, von abstrakt nach konkret. Änderungen kaskadieren abwärts.

```
Ebene  Typ                Dateien                             Inhalt
─────  ────────────────   ──────────────────────────────────  ─────────────────────────
  1    Weltbibel          00-welt.md, moragh-karte.json       Figuren, Welt, Orte. SoT.
  2    Regelsysteme       01-stil.md, 01-autorin-stimme.md    Stil, Magie, Stimme.
                          02-stilregeln-v2.md, 10-magie.md
  3    Charakter          11-nyr.md, 13-talven.md, pov/*.md   Figuren-Dossiers.
  4    Storyline          00-storyline.md                     Gesamtbogen.
  5    Zeitleiste         zeitleiste.json, status.json        SoT: Reihenfolge, POV, Events.
                                                             GEWINNT bei Konflikten.
  6    Aktpläne           04-akt3.md, 05-akt4.md              Beats, Tschechow für offene Kapitel.
  7    Entwürfe           kapitel/{ID}-entwurf.md             Plot → Prosa, Szenen inline.
  8    Finale Kapitel     kapitel/{ID}-{name}.md              Was die Leserin liest.
```

**Aktpläne Akt 1+2 sind archiviert.** Für alle finalen Kapitel (K1-K22 + I1-I3) hat das finale Kapitel Vorrang — Aktplan `02-akt1.md` und `03-akt2.md` wurden am 22. Apr 2026 nach `buch/_archiv/` verschoben. Der Kontext-Extraktor (`scripts/kapitel-kontext.py`) greift für diese Kapitel weiter auf das Archiv zu, falls nötig.

**Szenenpläne entfallen.** Die alten `buch/szenen/`-Pläne wurden am 26. Apr 2026 entfernt. Die detaillierten Szenen-Beats leben jetzt inline im jeweiligen Entwurf (`## Szene 1 — ...` mit Wortziel, Beats, Tschechow-Waffen, Dialog-Infos).

**Kaskaden-Regel:** Änderung auf Ebene N invalidiert N+1 bis 8. Abwärts durcharbeiten.

## Zuständigkeits-Map (Single Source of Truth)

Jede Regel hat **genau eine Master-Datei**. Andere Stellen (CLAUDE.md, Konkretheits-Referenz, Skill-Files in `.claude/commands/`) enthalten **nur Verweise auf den Master**, keine eigene Definition. Drift verhindern: bei Konflikt gewinnt der Master.

| Regel-Bereich | Master-Datei | Was hier definiert wird |
|---|---|---|
| Marktposition, Zielgruppe, Heat-Level-Kategorien, Stilvektoren | `buch/00-positioning.md` | Commercial-Positionierung, Referenz-Autoren-Tabellen, 95%-Gate. Bei Konflikt mit anderen Docs gewinnt Positioning. |
| Stilregeln (harte Limits, Default-Deny, Negation, Antithese, Stakkato, Konkretheits-Regeln, POV-Vokabular, Dialog-Limits) | `buch/02-stilregeln-v2.md` | Alle messbaren Regeln und Schwellen. Master für Stil-Verbote. |
| Autorin-Stimme (drei Register, Begehren-Vokabular pro POV, Anti-Patterns, Erotik-Regeln, Heat-Level pro Szene, Referenz-Autoren-Anwendung) | `buch/01-autorin-stimme.md` | Stimme und Ton, Pflicht-Adjektive pro POV, Anti-Patterns aus Council-Findings. |
| Konkretheits-Handwerk (Material-Erstnennung, Vorfeld-Inversion, Sinnes-Trias, Körper-als-Subjekt, FIR) | `buch/01-referenz-konkretheit.md` | Handwerks-Kanon. Konkretheits-Schwellen selbst stehen in Stilregeln. |
| Magie-System (Resonanzen, Kopplung, Verstärker, Velmar-Standards) | `buch/10-magie-system.md` | Mechanik, Limits, Bauarten. |
| Welt-Kanon (Orte, Monate, Pflanzen, Fraktionen, Technologie) | `buch/00-welt.md` + `buch/zeitleiste.json` | Kanonische Welt-Fakten. Zeitleiste GEWINNT bei Konflikten mit Prosa. |
| Figuren-Dossiers (Berufslinse, Sprach-Signatur, Wissensstand, Tschechow-Waffen) | `buch/pov/<figur>.md` | Pro POV-Figur ein Dossier. |
| Kapitel-Pipeline (Phasen, Skills, Modelle, Status-Kette) | CLAUDE.md (kompakt) + Skill-Files unter `.claude/commands/` | Pipeline-Logik in den Skills, Übersicht hier. |
| Skill-Anweisungen (Phasen-Logik, Subagent-Prompts, Output-Formate) | `.claude/commands/<skill>.md` | NUR Anwendungs-Logik. **Keine Regel-Definitionen** — Skills referenzieren die Master oben. |

**Verweis-Pattern bei Wiederholung:** Wenn eine Regel an mehreren Stellen erwähnt werden muss (z.B. weil ein Skill sie zur Laufzeit prüft), verweist die Sekundär-Stelle mit einer Zeile auf den Master:

> *„Master: `buch/02-stilregeln-v2.md` (Tabelle ‚Harte Limits' — &lt;Regelname&gt;)."*

Keine inhaltliche Wiederholung der Regel an der Sekundär-Stelle. Inhalt nur an einer Stelle pflegen.

## Kapitel-Pipeline (v2)

Drei Phasen mit Session-Breaks. Details in den jeweiligen Skill-Dateien (`/entwurf`, `/ausarbeitung`, `/lektorat-fix`).

**Kontext-Extraktor:** `python scripts/kapitel-kontext.py {ID} --phase entwurf|ausarbeitung|lektorat` liefert kapitelspezifische Slices aus zeitleiste.json + status.json (~3k statt ~51k Tokens). **Immer verwenden statt Dateien direkt zu laden.**

**NICHT direkt laden:** `zeitleiste.json`, `status.json`, `kapitel-summaries.md`, Aktpläne komplett. Der Extraktor liefert was gebraucht wird.

**Status-Kette:** `idee → entwurf → entwurf-checked → entwurf-ok → ausarbeitung → final` (seit 2026-04-26: Status `lektorat` entfaellt — `/ausarbeitung` setzt direkt `final`, weil das absatzweise Schreiben mit Mini-Council bereits Final-Niveau liefert.)

**Modelle:** `/entwurf` = Sonnet, `/ausarbeitung` = Opus, `/lektorat-fix` = Sonnet/Haiku (Mikro-Fixes auf finalen Kapiteln nach Online-Lesen).

## Kapitel-Header

Neue Kapitel: `# B1-K{KK} — {Figurname}` + `*{Tag}. {Monat} 551 · {N} Wochen {M} Tage in Vael*`
Alte Kapitel (1-11, I1, I2): `# {Figurname}` + `*{Tag}. {Monat} 551 · {Zeitangabe}*`

Ankunftstag = Tag 1. Wochen = floor(Tage/7), Rest = Tage%7.

**Monatsnamen (thalassisch, kanonisch):** Eismond, Sturmmond, Saatmond, Grünmond, Blütenmond, Lichtmond, Glutmond, Erntemond, Herbstmond, Nebelmond, Frostmond, Dunkelmond. Realweltliche Monatsnamen (Januar, März, Mai…) sind **überall verboten** — in Headern, in Prosa, in Dialogen. Gilt rückwirkend auch für K1-K11 und I1/I2. Volle Liste in `zeitleiste.json` (tz_kalender).

## Website

Deploy: `git push` (Hook deployed automatisch via generate-lesen.sh)

**Deploy-Regel:** Nach jeder Dateiänderung sofort committen und deployen.

## Sprache

Deutsch. Umlaute verwenden. Kein ae/oe/ue.
