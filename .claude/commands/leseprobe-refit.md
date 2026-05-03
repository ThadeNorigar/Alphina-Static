# /leseprobe-refit — Leseprobe sequenziell durch 4-Schritt-Refit-Pipeline

**Master-Pipeline:** Memory-Direktive `~/.claude/.../memory/feedback_leseproben_pipeline.md` (⚡-Pin in MEMORY.md). Dieser Skill ist nur die Anwendungs-Logik — die Pipeline-Definition lebt im Memory. Bei Konflikt gewinnt das Memory.

**Findings-Format-Pflicht:** Master = `buch/_findings-format.md`. Subagent-Findings + Konsolidierungs-Master-Tabelle in Schritt 4 im Block-Format mit Vorher/Nachher und Satz-Kontext, Tags `[PFLICHT]`/`[TIC]`/`[STIL?]`, Funktional-Filter PFLICHT vor jedem Tag, drei Bloecke (PFLICHT/EMPFEHLUNG/STIL-VORBEHALT). Quellen-Vergleich strikt asymmetrisch („Was die Quelle besser macht").

**Tracker:** `buch/leseproben/_status.md` — Status-Tabelle, Wellen-Plan, Quellen-Anker. Bei jedem Phasen-Wechsel aktualisieren.

**Modell-Soll:** Opus (Hauptsession). Synthese aus 6 Subagenten-Outputs + Konflikt-Hierarchie + Bild-Logik-Mini-Check ist kognitiv anspruchsvoll. Subagenten laufen auf general-purpose.

## Input

`$ARGUMENTS` = Probennummer als 1-2-stellige Zahl (`5`, `12`, `27`).

Wenn kein Argument: frage welche Probe. Verfuegbare Proben aus `buch/leseproben/_status.md` listen.

## Phase 0: Guard-Checks

### 0.1 Probe existiert?

`buch/leseproben/{NN}-*.md` per Glob aufloesen. Genau eine Datei → weiter. Mehr als eine → Liste anzeigen, abbrechen. Keine → Abbruch mit Probe-Liste.

### 0.2 Status-Check

`buch/leseproben/_status.md` lesen, Zeile `| {NN} | …` greifen.

| Status | Verhalten |
|---|---|
| `⏳ offen` | Normal weiter — Schritt 1 |
| `🔄 in Arbeit` | Frage: „In Arbeit. Schritt erkennen aus `_neuschrieb-{NN}.md` vorhanden? → Schritt 3 starten / Schritt 2 weiter / Neu starten?" |
| `✅ erledigt` | Frage: „Probe ist erledigt (Score X, Datum Y). Trotzdem refitten? Bei Ja: alte Version → Backup, neue Iteration vN+1 starten" |

### 0.3 Quellen-Anker pruefen

Aus `_status.md` Tabelle Zeile `{NN}`: POV, Heat-Level, Primaer-Referenz, Sekundaer-Referenz auslesen. Wenn Primaer als „(X fehlt)" markiert ist (z.B. Robert/Reisz/Morrison/Pierce Brown/Kuang) → Hinweis: „Primaer-Anker fehlt. Mit Sekundaer-Anker durchfuehren, klar markieren."

### 0.4 SLY-Sekundaer-Direktive

BDSM-Stellen (04, 05, 06, 25, 27) und Captivity-Power-Dynamik (26): SLY ist Pflicht-Sekundaer (User-Direktive 2026-05-03). Sicherstellen, dass Subagent-Prompt das aufgreift.

## Schritt 1 — Neuschrieb-Subagent

**Output:** `buch/leseproben/_neuschrieb-{NN}.md`

Subagent (`general-purpose`) erhaelt einen self-contained Prompt mit folgenden Pflicht-Komponenten — Pipeline-Mechanik aus Memory `feedback_leseproben_pipeline.md` und alle relevanten Memory-⚡-Pins inline einfuegen, NICHT nur referenzieren:

**1. Auftrag und Output:**
- Probe `buch/leseproben/{NN}-{kategorie}.md` komplett neu schreiben
- Output: `buch/leseproben/_neuschrieb-{NN}.md` mit Frontmatter aus Original + Zeile `version: neuschrieb` + `basiert_auf: {NN}-{kategorie}.md (vN)` + `quellen_lage: {kurzer Stand zu was gefunden/fehlend war}`
- Ziellaenge: Original-Korridor +/- 30%. Bei Heat-Level „explizit" oder „Gewalt" darf ueber Original hinaus, aber Begruendung im Output-Bericht
- Kein Findings-Bericht, kein Vergleich alt/neu — das macht Schritt 3

**2. Pflicht-Reads (zwingend, vollstaendig):**
- Original (`buch/leseproben/{NN}-*.md`)
- Master-Files: `buch/00-positioning.md`, `buch/02-stilregeln-v2.md`, `buch/01-autorin-stimme.md`, `buch/01-referenz-konkretheit.md`, `buch/00-welt.md`
- POV-Dossier: `buch/pov/{POV}.md` + ggf. Schreibblatt (`buch/pov/{POV}-schreibblatt.md`)
- Findings-Format: `buch/_findings-format.md`
- Status-Tracker: `buch/leseproben/_status.md` (fuer Vorgaenger-Versions-Lerneffekte)

**3. Quellen-Hebel (Reads aus `buch/referenzen/`):**
- Primaer-Referenz: `Leseprobe {RY|JM|SLY|Reage}.txt` + zugehoerige `*-stil-analyse.md` — Hebel-Liste extrahieren
- Sekundaer-Referenz(en): wie Primaer
- Bei BDSM/Captivity-Probe: SLY ist Pflicht-Sekundaer (Koerperteil-Subjekt-Praezision, Material-Funktionsname, dunkler Untergrund)

**4. Inline-Checkliste (vollstaendig im Subagent-Prompt zitieren):**

Welt-Canon-Verbote:
- KEINE Kirchen/Tempel/Liturgie/Sakrament/Priester/Goetter — areligioeser Gruendungskanon
- KEINE realweltlichen Monatsnamen (Mai → Bluetenmond etc., siehe `00-welt.md` tz_kalender)
- KEINE Magie-Imperative wie Hund-Kommando — Magie via Wille+Vorstellung
- KEIN „Resonanz" in Prosa — Canon-Begriff, draussen
- KEINE Schemen-Benennung in Prosa
- KEINE Anglizismen, fruehes 19. Jhd. Register
- KEINE Jacke/Bluse — Kleidungs-Canon (Mantel/Hemd/Tunika/Rock/Westen)

POV-Verbote (allgemein):
- KEINE Cross-POV-Mindreading
- KEIN „nicht X, sondern Y"-Tic — Default streichen
- KEIN „halb X" ausser kanonisch (Masse, Velmar-Ritual)
- KEIN „fast X" als verwandte Klischee-Klasse
- KEIN Selbstkommentar-Schleife („sie wusste, dass sie nicht…")
- KEIN Aphorismus am Absatzende ohne Beat („Das war Y.")
- KEIN „Puls" als abstraktes Substantiv — Halsschlagader/Kehle/Handgelenk konkret
- KEIN „und das aergerte/freute/erschreckte sie" (Autoren-Sicherung)
- KEINE Adverb-Tags / Denk-Tags / Foto-Vokabular auf Gesicht
- KEINE benannte Emotion als Substantiv (Sehnsucht/Obsession/Scham)
- KEINE sinnfreie Negationen
- KEINE Default-Sein-Verben als Tic (lag/war/stand/sass)
- KEINE Substantiv-Phrasen ohne Verb als Default — vollstaendige Saetze als Default
- KEINE Stakkato-Ketten ohne Pflicht-Begruendung pro Einsatz

POV-spezifisch (passend zur Probe einfuegen):
- **Alphina:** keine Uhrmacher-Praezision, Berufslinse Botanikerin 15-20%, Innenstimme nuechtern/klinisch/kontrolliert; sparsame kursive Innen-Spitzen erlaubt
- **Sorel:** glatt rasiert, in Intimitaet riecht/schmeckt nach Haut/Leinen/Abendluft (NICHT Pyrogallol/Fixiersalz), Alphina/Sorel kein BDSM
- **Maren:** Werftsalz/Meersalz-Register, Wasser-Resonanz vier Modi (Steuern/Kochen/Vereisen/Hoeren)
- **Vesper:** Uhrmacher-Berufslinse (Toleranz/Passung/Mechanik)

Bild-Logik-Pflicht:
- Jede Metapher/jeder Vergleich auf innere Logik pruefen vor dem Schreiben
- Verb muss zum gemeinten Bild passen (Trockenheit „klemmt" nicht)
- Verb-Praezisierung: Default-Verben (sein/haben/machen/gehen/legen/setzen/nehmen/geben/lassen/halten/tun/kommen) durch praezisere Verben ersetzen, wo immer es traegt

**5. Output-Bericht (an Hauptsession):**
- Pfad und Wortzahl
- 3-5 Saetze: welche Quellen-Hebel wo angewandt
- Offene Punkte / fehlendes Quellen-Material

## Schritt 2 — Autor-Abnahme

**STOP. Hauptsession wartet.**

- Pfad zum Neuschrieb melden
- Subagent-Bericht weiterreichen
- Frage: „OK fuer Schritt 3, oder Korrekturen?"
- Bei Korrekturen: zurueck zu Schritt 1, neuer Subagent-Lauf mit den Korrektur-Direktiven inline im Prompt
- Bei OK: weiter zu Schritt 3

`_status.md` updaten: `🔄 in Arbeit · Schritt 2 abgeschlossen`

## Schritt 3 — Refit-Pipeline + Vergleich (6 parallele Subagenten)

Alle 6 Subagenten gleichzeitig dispatchen (Single-Message-Multi-Tool-Use). Jeder Subagent erhaelt:
- Auftrag + Probennummer + Pfad zum Neuschrieb
- Pflicht-Reads (eigene Master-Files passend zur Rolle)
- Auftrag, Findings strikt nach `buch/_findings-format.md` Block-Format zu liefern
- Pflicht-Lob-Tabelle, wenn Genre-Leserin oder Vergleichs-Subagent
- Asymmetrische Quellen-Vergleichs-Tabelle, wenn Vergleichs-Subagent

### Subagent-Roster

**A: Sprach-TUEV**
- Reads: `02-stilregeln-v2.md`, `01-autorin-stimme.md`, `01-referenz-konkretheit.md`, `_findings-format.md`
- Aufgabe: Verstoss-Liste gegen Stilregeln-Master, gefiltert durch Funktional-Filter (4 Fragen). Tags `[PFLICHT]/[TIC]/[STIL?]`. Findings im Block-Format.

**B: Verquastungs-Detektor**
- Reads: `02-stilregeln-v2.md` (10-Punkt-Lese-Test), `_findings-format.md`
- Aufgabe: 10-Punkt-Test pro Satz. Pseudo-Logik, leere Verben, „Nichts"-als-Material, abstrakte Substantive, Pseudo-Praezision. Findings im Block-Format.

**C: Konsistenz/Logik**
- Reads: POV-Dossier `buch/pov/{POV}.md`, `00-welt.md`, `_findings-format.md`, ggf. Magie-System `10-magie-system.md`
- Aufgabe: POV-Stimme, Wissensstand, Beat-Logik, Welt-Canon, Magie-Mechanik. Findings im Block-Format mit `[PFLICHT]` fuer Canon-Bugs.

**D: Genre-Leserin** — passend zu Heat-Level der Probe:
- `leise/commercial/explizit non-BDSM` → **LINA** (Romantasy-Leserin 28J, Yarros/Maas-erfahren)
- `explizit BDSM/leise BDSM` → **MEIKE** (BDSM-Leserin 35J, Reage/Rampling-erfahren)
- `Drohung/Action/Trauer` → **VICTORIA** (Dark-Fantasy-Leserin 32J, Kuang/SenLinYu-erfahren)
- `Gewalt` → **KAYA** (Grimdark-Leserin 30J, Abercrombie/Lawrence-erfahren)
- Reads: Heat-Level-Definitionen aus `00-positioning.md`, `_findings-format.md`
- Aufgabe: subjektive Lese-Reaktion, was traegt/was zieht raus. Pflicht-Lob-Tabelle (min. 5 Stellen). Score 0-100% am Ende.

**E: Vergleichs-Subagent (Original vs Neuschrieb)**
- Reads: Original (`{NN}-*.md`), Neuschrieb (`_neuschrieb-{NN}.md`), Quellen-Hebel-Tabellen (Primaer + Sekundaer aus `buch/referenzen/`), `_findings-format.md` Sektion „Quellen-Vergleich"
- Aufgabe — fokussiert auf 3 Aspekte (KEINE Mikro-Findings, die A/B besser machen):
  1. Asymmetrische Quellen-Hebel-Tabelle: welche Quellen-Hebel sind angekommen? Welche fehlen?
  2. Original-Staerken-Erhalt: was hatte das Original, das der Neuschrieb verloren hat?
  3. Quellen-Defizit-Liste mit Uebernahme-Vorschlaegen — Format `| Hebel | Quelle (Z.) | Quell-Beispiel | Defizit | Konkrete Uebernahme |`
- Pflicht-Format: asymmetrisch, „Was die Quelle besser macht" — keine Selbstbestaetigungs-Tabelle.

**F: Bild-Logik + Verb-Praezision**
- Reads: Memory `feedback_bild_logik_verb_praezision.md` (vollstaendig zitieren im Prompt), `_findings-format.md`
- Aufgabe — zwei Layer:
  1. Bild-Logik: jede Metapher/jeder Vergleich auf innere Logik pruefen (passt das Bild im Detail? funktioniert die Verschraenkung?)
  2. Verb-Praezision: jedes Default-Verb (sein/haben/werden/machen/gehen/legen/setzen/nehmen/geben/lassen/halten/tun/kommen/liegen/sehen/fuehlen/finden/bekommen/merken/wurden) auf Tic-Charakter pruefen, praezisere Alternative vorschlagen
- Findings im Block-Format. PFLICHT — kein Cherry-Picking durch Hauptsession.

`_status.md` updaten: `🔄 in Arbeit · Schritt 3 laeuft`

## Schritt 4 — Final-Abnahme

Hauptsession konsolidiert die 6 Subagenten-Outputs zu einer **Master-Tabelle in 3 Bloecken** nach `_findings-format.md`:

- **Block A — PFLICHT** (Konsistenz/Canon-Verstoss + klare Stilregel-Verletzungen ohne Funktion)
- **Block B — EMPFEHLUNG** (klarer Stil-Tic, keine Funktion)
- **Block C — STIL-VORBEHALT** (formal Verstoss, Funktion da)

Plus: **Quellen-Vergleichs-Tabelle** vom Vergleichs-Subagent (E) — separat, asymmetrisch, mit Uebernahme-Liste.

Plus: **Pflicht-Lob-Tabelle** vom Genre-Leserin-Subagenten (D) — separat.

### Konflikt-Hierarchie (Pflicht)

Wenn Genre-Leserin (D) oder Vergleichs-Subagent (E) eine Stelle als positiv markieren, die Sprach-TUEV (A) oder Konsistenz (C) als PFLICHT markiert haben → automatisch in Block C (STIL-VORBEHALT), nicht Block A. Hauptsession entscheidet im Zweifel zugunsten Block C.

### Hauptsession-Bild-Logik-Mini-Check (Pflicht vor jedem Edit-Vorschlag)

Pro Verb-Ersetzung gegen Bild-Logik pruefen. Beispiel: bei „Ihre Kehle war trocken" → nicht „klemmte Trockenheit" (Trockenheit klemmt nicht), sondern „Sie schluckte trocken" (Aktion-Verb mit Bild-Logik).

### Subagent-F-Output ist PFLICHT

Lerneffekt Probe 03: Hauptsession muss alle Verb-Praezisions-Findings durchziehen, nicht selektiv. Plus zusaetzlicher Verb-Sweep durch die Hauptsession nach Konsolidierung — durch den ganzen Text, alle Default-Verben pruefen. Beispiele aus Probe 03: lag→fiel/pulsierte, gab→wandte/entwich, fanden→tasteten nach, bekam→loeste, war heiss→brannte. „Aber das Default-Verb ist idiomatisch ok" ist KEINE Begruendung — praeziser ist immer besser.

### Autor-Workflow

- Master-Tabelle + Quellen-Vergleich + Lob-Tabelle praesentieren
- Autor entscheidet pro Finding `ok` / `skip` / eigener Fix
- Findings einarbeiten in `_neuschrieb-{NN}.md` (Edit, mit Bild-Logik-Mini-Check)
- Final-Abnahme: Autor liest Endfassung, gibt OK
- Original `{NN}-{kategorie}.md` mit finalem Text ueberschreiben (Frontmatter von Original behalten, ggf. `canon_status` aktualisieren)
- `_neuschrieb-{NN}.md` loeschen
- `_status.md` updaten: `✅ erledigt · vN · {Score} · {Datum} · {Notiz}`

### KEIN Commit, KEIN Deploy

Sammel-Commit + Deploy erst am Ende aller 35 Proben (siehe `_status.md`). Nicht zwischendurch.

## Hauptsession-Disziplin (Pflicht)

- Keine Volltext-Reads von Quellen oder Mastern in der Hauptsession
- Keine Volltext-Reads der Stil-Analysen ausser einmal initial (Uebersicht)
- Subagenten kapseln den Kontext
- Hauptsession nur: Status-Datei pflegen, Subagenten dispatchen, User-Output praesentieren, Finalisieren

## Zustaendigkeiten / Master-Verweise

- Pipeline-Definition: Memory `feedback_leseproben_pipeline.md` (⚡-Pin)
- Bild-Logik + Verb-Praezision: Memory `feedback_bild_logik_verb_praezision.md` (⚡-Pin)
- Findings-Format: `buch/_findings-format.md`
- Stilregeln-Master: `buch/02-stilregeln-v2.md`
- Autoren-Stimme: `buch/01-autorin-stimme.md`
- Konkretheit: `buch/01-referenz-konkretheit.md`
- Positioning: `buch/00-positioning.md`
- Tracker: `buch/leseproben/_status.md`
- Quellen: `buch/referenzen/Leseprobe {RY,JM,SLY,Reage}.txt` + `*-stil-analyse.md`

Aenderungen an Pipeline-Mechanik gehoeren ins Memory, nicht in diese Datei. Dieser Skill spiegelt das Memory.
