# /refit — Alt-Kapitel auf aktuellen Stil bringen

**Ziel:** Ein Kapitel aus der alten Aera (vor April 2026) in den aktuellen commercial-Dark-Romantasy-Stil ueberfuehren — durch **Plot-Lock-Extraktion plus Neuausarbeitung**. Kein Edit-in-place.

**Warum ein eigener Skill:** `/ausarbeitung` setzt einen freigegebenen `/entwurf` voraus. Alte Kapitel (K01-K04, K06-K08) haben keinen Entwurf mehr — der Plot steckt in der Prosa. Ein Edit-Pass auf der Altprosa produziert Mongrel-Text (Claude-Code-Falle). `/refit` extrahiert stattdessen die Beats in ein **Plot-Lock-Dokument**, generiert daraus einen regulaeren Entwurf, archiviert das Altkapitel und uebergibt an die bestehende `/ausarbeitung`-Pipeline.

**Modell-Soll:** Sonnet (Hauptsession). Plot-Extraktion ist kognitive Arbeit, keine Prosa. Subagenten explizit per Override.

## Input

`$ARGUMENTS` = Kapitel-ID im alten oder neuen Format:
- `01-alphina` / `02-sorel` (alter Dateiname ohne Endung)
- `B1-K01` (neue Form, wird auf alte Datei aufgeloest)

Wenn kein Argument: frage welches Kapitel.

## Phase 0: Guard-Checks

### 0.1 Modell-Check

Wenn nicht Sonnet:

> WARNUNG: Du bist auf [Modell]. Diese Phase ist Plot-Extraktion, keine Prosa. Auf Opus zahlst du den Aufpreis ohne Mehrwert. Auf Haiku leidet die Qualitaet der Beat-Abstraktion. Empfehlung: Session beenden, neu starten mit `claude --model sonnet`. Trotzdem weiter?

Auf Opus: warten auf explizites "weiter". Auf Haiku: zwei Bestaetigungen.

### 0.2 Altkapitel existiert?

Pruefen: `buch/kapitel/{alte-datei}.md` vorhanden?

- `01-alphina.md`, `02-sorel.md`, ..., `04-maren.md`, `06-sorel.md`, `07-vesper.md`, `08-maren.md` — alte Numerierung
- Wenn nein: HARTER ABBRUCH: "Altkapitel-Datei nicht gefunden. Welches Kapitel willst du refitten? Verfuegbar: [Liste aus ls buch/kapitel/ ohne entwurf/szene/handoff/legacy]"

### 0.3 Status-Check

Aus `status.json` lesen.

| Aktueller Status | Verhalten |
|---|---|
| `final` oder `lektorat` (Alt-Stil) | Normal weiter |
| `entwurf-ok` / `ausarbeitung` | HARTER ABBRUCH: "Kapitel ist schon in der neuen Pipeline. /refit ist fuer Alt-Kapitel." |
| `refit` (in Arbeit) | Frage: "Refit laeuft schon. Plot-Lock neu erstellen (ueberschreiben) oder weiter?" |

### 0.4 Stil-Gap-Check (diagnostisch, unverbindlich)

Kurzer Grep-Check auf typische Alt-Stil-Marker im Altkapitel:
- `nicht X — sondern Y` / `nicht X, sondern Y`
- `sie dachte` / `er fragte sich`
- `Das war` am Absatz-Anfang oder -Ende
- Abstrakta-Stapel: `der/die/das [Stille|Kaelte|Schwere|Leere|Ferne] des/der`
- Satz mit `wie etwas, das...`

Wenn Summe < 3 Treffer: Warnung ausgeben: "Stil-Gap schwach. Ist dieses Kapitel wirklich alt? Ergebnis pruefen, dann bestaetigen."

Diese Pruefung blockiert nicht — sie verhindert nur versehentliche Refits von bereits modernen Kapiteln.

### 0.5 Parameter-Normalisierung

Aus Dateiname `NN-figur.md` → `B1-K{NN}` ableiten. POV-Figur aus Dateiname (`01-alphina` → Alphina). Fuer Interludien gesondert.

## Phase 1: Kontext laden — Extraktions-Setup

**Schritt 1: Kontext-Extraktor ausfuehren (Bash):**

```bash
python scripts/kapitel-kontext.py {ID} --phase entwurf
```

Liefert Timeline-Anker, Nachbar-Kapitel, Events, Wissensstand der POV-Figur an diesem Datum. Ersetzt direkte zeitleiste.json/status.json-Reads.

**Schritt 2: Parallel mit Read laden:**

1. **`buch/00-positioning.md` ZUERST** (~800 W — Marktposition, Heat-Regeln, 95%-Gate)
2. `buch/02-stilregeln-v2.md` (~5k W — harte und dosierte Limits, Konkretheits-Regeln, POV-Vokabular)
3. `buch/01-autorin-stimme.md` (~4.5k W — Autor-Stimme, Begehren-Vokabular, Anti-Patterns)
4. `buch/kapitel/{alte-datei}.md` — **Extraktions-Quelle**, der Altkapitel-Text
5. `buch/pov/{figur}.md` — POV-Dossier (~500 W)
6. `buch/00-canon-kompakt.md` (~800 W — Welt/Figuren auf einen Blick, fuer Canon-Abgleich)

**NICHT laden (kommen spaeter):**
- Andere Altkapitel — nur das zu refittende
- Leseproben-Volltexte — erst in Phase 4 (Anker-Auswahl)
- Voice-Referenz-Kapitel — erst in `/ausarbeitung`
- `buch/zeitleiste.json`, `buch/status.json` direkt — Extraktor liefert das
- `buch/kapitel-summaries.md` — redundant zum Extraktor-Output
- Aktplaene komplett — Extraktor liefert Snippet

**Ziel-Kontext: ~13-16k W.** Extraktor (~3k) + Positioning (~800) + Stilregeln (~5k) + Autor-Stimme (~4.5k) + Altkapitel (~3-6k je nach Laenge) + POV (~500) + Canon-Kompakt (~800).

## Phase 2: Plot-Lock schreiben

Datei: `buch/kapitel/{ID}-plot-lock.md`

Der Plot-Lock ist **Canon-Dokument** — er bleibt nach dem Refit liegen als definitive Referenz fuer den Kapitel-Inhalt. Jeder darin notierte Beat und jedes Tschechow-Element MUSS im refitteten Kapitel landen.

**Format strikt:**

```markdown
# {ID} — {Figur} — Plot-Lock

**Quelle:** buch/kapitel/{alte-datei}.md
**Extraktionsdatum:** {ISO-Datum}
**POV:** {Figur} (3. Person nah, Praeteritum)
**Timeline-Anker:** {Tag. Monat 551} · {N Wochen M Tage in Vael / Ort}
**Wortziel Refit:** 4.000-4.500 W

## Canon-Gewaehr

Ein Absatz (50-120 W): Was muss aus dem alten Kapitel zwingend ueberleben? Worum geht es in diesem Kapitel im Plot-Canon? Welches Tschechow-Element feuert hier oder wird hier geladen?

## Szenen-Struktur

- Szene 1: {Kurztitel} · {Ort} · {Uhrzeit} · {Register-Soll} · {Heat-Level}
- Szene 2: ...
- Szene 3: ...
- (2-4 Szenen)

---

## Szene 1 — {Titel}

**Ort:** {exakt — Wohnung 4. Stock, Garten der Gesellschaft, etc.}
**Zeit:** {Tageszeit, wenn im Text genannt: "12 Minuten nach drei"}
**Register-Soll:** {Mischung aus langsam/normal/schnell}
**Heat-Level:** {keine / leise / commercial / explizit non-BDSM / explizit BDSM / Drohung / Gewalt}
**Wortziel:** {~1.200-1.600}

### Plot-Beats (harte Reihenfolge)

1. {Beat 1 — was passiert konkret, in einem Satz}
2. {Beat 2}
...
N. {Beat N}

### Tschechow-Elemente

Konkrete Dinge/Details aus dem Altkapitel, die als Tschechow-Waffen fungieren — entweder hier geladen oder hier abgefeuert.

| Element | Zeile alt | Funktion | Zuendet in | Bleibt? |
|---------|-----------|----------|------------|---------|
| Wetterfahne Hand-nach-Norden | 19 | Vael-Unheimlichkeit | K?? | ja |
| 49 Pflanzen | 15 | Figurentreue | laufend | ja |
| Laris-Hand-am-Bauch | 55 | Beziehungs-Backstory | K?? | ja |
| Oolong 85°C | 47 | Kontroll-Tic | laufend | ja |

### Sinnes-Inventar (spezifische, nicht-generische Details)

Liste aller im Altkapitel benannten konkreten Details mit Zahlen/Namen/Material. Nicht "die Nacht war dunkel", sondern "vier Stockwerke unter ihr", "drei violette Bluete", "fuenfundvierzig Turmuhren, das Gildehaus geschlossen seit achtzig Jahren".

- {Detail 1}
- ...

### Gefühls-Wirkung (wechselseitig) — PFLICHT

**Gegenpol zur emotionalen Einseitigkeit.** In jeder Szene mit zwei oder mehr Figuren muss sichtbar werden, **dass und wie die Figuren einander verändern** — durch Körper, nicht durch benannte Gefühle.

- **Was macht das Gegenüber mit der POV-Figur?** Min. 2 Körper-Beats in ihr, die zeigen: eine Geste/Äußerung/Reaktion des anderen landet. Unterbauch, Kehle, Gesicht, Atem, Hand-die-länger-bleibt-als-nötig, Puls, Hitze, Zittern, Stimme, die durchbricht.
- **Was macht die POV-Figur mit dem Gegenüber?** Min. 2 sichtbare Reaktionen im anderen, die die POV-Figur wahrnehmen kann (Atmen-tiefer, Zucken, Haltung, Geräusch, Blick, Finger-die-greifen-ohne-Ziel). Kein Mindreading — nur was sichtbar ist.
- **Bei Alleinszenen (Alphina allein in K01):** Wirkung der Welt/Magie/Erinnerung auf die Figur. Laris-Erinnerung → Körper. Warme Erde → Unterbauch, Hand-zieht-sich-weg. Mindestens 2 Körper-Beats, die zeigen, dass die Figur von etwas bewegt wird.

**Pflicht-Frage beim Refit:** Wo ist {POV-Figur} emotional getroffen in dieser Szene? Wenn die Antwort "wird geführt, beobachtet, registriert" ist — **Defizit**. Auch ohne benannte Emotionen muss Wirkung sichtbar sein.

Hintergrund: Commercial Dark Romantasy lebt von wechselseitiger Verletzbarkeit. Wenn eine Figur Regisseur/Beobachter ist und die andere alle Körperreaktionen trägt, kippt es in einseitiges BDSM-Register (auch wenn kein BDSM-Canon gilt). Gegenmittel: Körper-Spiegel-Beats, Wirkung aus Gesten-des-anderen, Heat an ungewohnten Stellen (Gesicht, Kehle, Ohren).

### Dialog-Beats (falls Dialog)

- {Figur A} sagt/erfaehrt: {Info}
- {Figur B} sagt/erfaehrt: {Info}
- {Innere Wendung am Szenen-Ende}

### Canon-Wissensstand am Ende der Szene

- **Weiss:** {was die POV-Figur jetzt sicher weiss}
- **Weiss nicht (Sorel-Prinzip):** {was ihr kuenftig begegnet, aber hier noch nicht}

---

## Szene 2 — ...

{analog}

---

## Szene 3 — ...

## Refit-Hinweise (Stil-Gap-Diagnose)

Konkrete Befunde aus dem Altkapitel, die beim Refit dringend anders werden muessen. Pro Befund: Zeile + Zitat + Problem + Richtung-des-Fixes. Pflicht-Kategorien zu pruefen:

- **Abstrakta-Stapel** (`Stille, Kaelte, Schwere, Leere, Ferne, Ewigkeit, Abgrund` in Ketten)
- **Scharnier-Aphorismen** (`X. Das war Y.` am Absatz-Ende)
- **Figur-redet-ueber-sich** (Selbstkommentar statt Koerperbeat)
- **Metapher + Erklaer-Nachsatz** (Bild wird verdoppelt)
- **Mindreading** (POV liest Motive anderer)
- **Benannte Emotionen als Substantiv** (Sehnsucht, Obsession, Scham, das Unheimliche)
- **Premature Doubt** (Figur zweifelt bevor Ausloeser da ist)
- **Chroniken-Prophezeiung** (Erzaehler weiss die Zukunft)
- **95%-Gate** (Eroeffnung: Hook, Wollen, Kipp-Moment, Koerper)
- **Berufslinsen-Ueberzug** (Linse als Karikatur statt 15-20% Anteil)
- **Komma-Listen-Katalog** (Koerperbeschreibung als Liste)
- **Emotionale Einseitigkeit** (eine Figur reagiert mit Koerper, die andere beobachtet nur — bei 2+ Figuren in einer Szene Defizit. Wirkung muss wechselseitig sein, siehe Gefühls-Wirkung oben.)

Wichtige Faelle konkret zitieren. Keine erschoepfende Tabelle — nur die, die beim Rewrite ins Auge fallen muessen.

## Gaensehaut-Moment

Was ist das Unmoegliche, das vor der Figur physisch passiert? Ein Satz. Pflicht pro Kapitel.

## Anker-Kandidaten (werden in Phase 4 finalisiert)

- **Register-Anker (Leseprobe(n)):** {Vorschlag aus buch/leseproben/}
- **Voice-Anker (Kapitel):** {letztes fertiges Kapitel derselben POV im neuen Stil}

```

## Phase 3: Plot-Lock mit Autor pruefen

**GATE: Dies ist der wichtigste Schritt des Refits. Hier wird entschieden, was der Plot des Kapitels tatsaechlich IST.**

Dem Autor zeigen:
1. Szenen-Struktur (Ueberblick)
2. Pro Szene: **Plot-Beats als nummerierte Liste** (nicht Prosa, sondern nackte Beats)
3. Tschechow-Tabelle (was bleibt, was kann weg)
4. Sinnes-Inventar komplett
5. Refit-Hinweise (Top-5 kritische Stil-Gaps)
6. Gaensehaut-Moment

**Fragen an den Autor:**

- Sind alle Plot-Beats erfasst? Fehlt einer?
- Stimmt die Szenen-Anzahl? Soll eine Szene geteilt/zusammengefasst werden?
- Welche Tschechow-Elemente bleiben? Welche fliegen raus? Gibt es neue, die nach heutigem Canon hinzukommen (z.B. Bezug auf spaetere Kapitel, die beim urspruenglichen Schreiben noch nicht existierten)?
- Heat-Level pro Szene OK?
- Register-Soll pro Szene OK?
- Gaensehaut-Moment trifft?
- Refit-Hinweise: noch was vergessen?

Aenderungen direkt im Plot-Lock einarbeiten, bis Autor "plot-lock ok" sagt.

**GATE: Ohne explizites "plot-lock ok" kein Phase-Wechsel.**

## Phase 4: Anker-Auswahl

Parallel drei Dateien lesen und vergleichen:

1. Vorschlag Register-Anker (Leseprobe) lesen
2. Vorschlag Voice-Anker (Kapitel) lesen
3. Plot-Lock lesen

**Pro POV-Figur Standard-Kandidaten:**

| POV | Voice-Anker (Kapitel) | Register-Anker (Leseproben) |
|-----|----------------------|------------------------------|
| Alphina | K05 oder K09 | 01 (Banter), 08 (Magie-Kontrollverlust), 09 (Vael warm), 11 (Moragh-Ankunft) |
| Sorel | K10 | 02 (erster Kuss), 03 (Heat explizit), 09 (Vael warm) |
| Vesper | K11 | 04 (BDSM-Alltag), 06 (Aftercare), 10 (Vael kalt) |
| Maren | noch keiner — Leseproben-Mix | 04 + 05 (BDSM), 09 (Werft warm), 06 (Aftercare) |

Passend zur Plot-Lock-Szene waehlen. **Heat-Level muss matchen** — keine explizit-BDSM-Leseprobe fuer Alltagsszene.

Dem Autor Vorschlag mit Begruendung vorlegen. **GATE: Autor bestaetigt Anker.**

## Phase 5: Entwurf im /entwurf-Format generieren

Datei: `buch/kapitel/{ID}-entwurf.md`

Aus Plot-Lock + Anker einen regulaeren Entwurf generieren (exakt im Format von `/entwurf` Phase 2). Kritisch: **Die Dialog-Info-Listen pro Szene muessen die Beats aus dem Plot-Lock 1:1 tragen.** Kein Beat darf still verloren gehen.

Zusaetzlich pro Szene ein Feld **Register-Vorgabe** mit Verweis auf konkrete Anker-Stellen:

> Register-Vorgabe: NORMAL-Mittelbau dominant, LANGSAM-Passage an Garten-Eintritt (vgl. Leseprobe 09 "Welt Vael warm" Zeilen X-Y), SCHNELL-Passage nur am Gaensehaut-Moment (vgl. K09-alphina Zeilen X-Y).

## Phase 6: Altkapitel archivieren

```bash
mkdir -p buch/kapitel/legacy
git mv buch/kapitel/{alte-datei}.md buch/kapitel/legacy/{alte-datei}.md
```

Anschliessend: Banner in der archivierten Datei einfuegen (Edit-Tool):

```markdown
> **LEGACY — REFIT DURCH /refit**
> Dieses Kapitel ist im alten Stil. Der Plot-Canon lebt in
> `buch/kapitel/{ID}-plot-lock.md`. Das neue Kapitel entsteht
> unter `buch/kapitel/{ID}-{figur}.md` durch `/ausarbeitung`.
> Diese Datei ist ab sofort **nicht mehr Canon** und wird nur
> als Tschechow-Referenz fuer den Refit gehalten.
```

## Phase 7: status.json aktualisieren

Felder fuer dieses Kapitel:
- `state: "entwurf-ok"` (damit /ausarbeitung starten kann)
- `entwurfs_datei: "{ID}-entwurf.md"`
- `plot_lock_datei: "{ID}-plot-lock.md"`
- `legacy_datei: "legacy/{alte-datei}.md"`
- `refit_gestartet: "{ISO-Datum}"`
- `datei: "{ID}-{figur}.md"` (fuer spaetere /ausarbeitung-Ausgabe)

## Phase 8: Handoff fuer /ausarbeitung

Datei: `buch/kapitel/{ID}-handoff.md`

```markdown
# Handoff — {ID}

**Von Phase:** refit → **Zu Phase:** ausarbeitung
**Erstellt:** {ISO-Datum}
**Status beim Handoff:** entwurf-ok

## Modell-Empfehlung

claude --model opus

## Aufruf fuer naechste Session

/ausarbeitung {ID}

## Kontext fuer naechste Session

- POV: {Figur}
- Wortziel: 4.000-4.500
- Timeline-Anker: {aus Plot-Lock}
- Freigegebener Entwurf: buch/kapitel/{ID}-entwurf.md
- **Plot-Lock (PFLICHT-READ in /ausarbeitung Phase 1):** buch/kapitel/{ID}-plot-lock.md
- **Register-Anker:** {Leseprobe(n)-Pfade}
- **Voice-Anker:** {Kapitel-Pfad}
- **Legacy-Referenz (nur fuer Tschechow-Beats, NICHT fuer Stil):** buch/kapitel/legacy/{alte-datei}.md

## Besondere Anweisungen

- Dies ist ein **REFIT**, keine Neuschrift aus dem Nichts. Jeder Plot-Beat aus dem Plot-Lock MUSS landen.
- Die Legacy-Datei darf **nicht** als Stil-Vorlage benutzt werden. Sie ist Tschechow-Spickzettel, mehr nicht.
- Bei Konflikt zwischen Plot-Lock und Legacy-Datei gilt Plot-Lock (er ist autorisiert durch "plot-lock ok").
- 95%-Gate (Positioning 9) pruefen, besonders fuer K01 (Buch-Oeffnung).
- Wenn `/ausarbeitung` findet, dass Plot-Lock luecken hat: **STOPP und Rueckkehr zu /refit**. Niemals Plot still anpassen.
```

## Phase 9: Harter Stop

```
REFIT VORBEREITET. Status: entwurf-ok.

Plot-Lock: buch/kapitel/{ID}-plot-lock.md
Entwurf: buch/kapitel/{ID}-entwurf.md
Legacy archiviert: buch/kapitel/legacy/{alte-datei}.md

Naechster Schritt: NEUE SESSION mit Opus.

1. Diese Session beenden
2. claude --model opus
3. /ausarbeitung {ID}

Das Handoff-File wird automatisch gelesen.

Diese Session schreibt jetzt nichts mehr.
```

## Sonderfall: K01 (Buch-Oeffnung)

K01 traegt besondere Last. 95%-Gate aus `00-positioning.md` Abschnitt 9 ist hier **ueberlebenswichtig**:
- Erster Satz = Hook (Figur in Situation mit Spannung, nicht Atmosphaere-Beobachtung)
- Figur will etwas, deutlich, in den ersten 50 Woertern
- Etwas passiert/kippt in den ersten 200 Woertern
- Koerper oder Emotion hoerbar im ersten Viertel

Im Plot-Lock fuer K01 **zusaetzlich** ein Abschnitt "Oeffnungs-Gate" mit:
- Vorschlag fuer den ersten Satz (Hook-Form)
- Wollen der Figur in Szene 1 (konkret benannt)
- Erster Kipp-Moment: wo?
- Erster Koerper-Marker: wo?

Ein `/book-council`-Durchlauf auf den Opening-Entwurf ist **empfohlen** vor `/ausarbeitung`.

## Sonderfall: POV ohne Voice-Anker (Maren)

Maren hat (Stand April 2026) kein fertiges Kapitel im neuen Stil — K04 und K08 sind beide alt. Bis das erste Maren-Kapitel im neuen Stil existiert, als Voice-Anker die **Leseproben 04 + 05 + 09** kombiniert nutzen, plus einen Satzlaengen-Hinweis aus `02-stilregeln-v2.md` (Maren ~35W, fliessend, Wasser-Metaphorik). Reihenfolge-Empfehlung: K04 refitten **bevor** K08, damit K04-refit dann selbst als Voice-Anker fuer K08 dient.

## Regeln

- **KEIN Edit-in-place.** Kein Satz aus dem Altkapitel darf automatisch ueberleben. Alles laeuft ueber den Plot-Lock.
- **Plot-Lock ist Canon.** Jeder Beat daraus MUSS in der neuen Prosa landen. Verlust = Regression.
- **Anker sind Ton-Referenz, kein 1:1-Vorbild.** Die Leserin erkennt den Ton, nicht Zitate.
- **Bei Beat-Luecke im Plot-Lock:** in Phase 3 den Autor fragen. Niemals still ergaenzen.
- **Bei Stil-Konflikt zwischen Altkapitel und aktuellen Stilregeln:** Stilregeln gewinnen. Das IST der Grund fuer den Refit.
- **Bei Plot-Konflikt zwischen Altkapitel und Plot-Lock:** Autor entscheidet in Phase 3. Plot-Lock ist die Gewalt-Frage, nicht die Stil-Frage.
- Deutsch. Umlaute verwenden (ä, ö, ü, ß). Kein ae/oe/ue in der Zielprosa — innerhalb dieses Skill-Dokuments selbst sind ae/oe/ue tolerierbar, aber der Plot-Lock und der Entwurf werden mit Umlauten geschrieben, weil die /ausarbeitung sie auch so erwartet.
- Setze `entwurf-ok` NUR nach "plot-lock ok" + generiertem Entwurf.
- Das Legacy-Kapitel bleibt fuer Tschechow-Referenz erhalten, aber nicht als Stil-Vorlage.

## Gates (Zusammenfassung)

| Gate | Bedingung |
|---|---|
| Altkapitel existiert | Sonst Abbruch |
| Plot-Lock "ok" | Explizites Autor-"plot-lock ok" vor Phase 4 |
| Anker bestaetigt | Explizites Autor-OK vor Phase 5 |
| Handoff geschrieben | Vor hartem Stop |

$ARGUMENTS
