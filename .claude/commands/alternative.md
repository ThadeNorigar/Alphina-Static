# /alternative — Varianten-Vergleich & Hybrid

Vergleiche eine an anderer Stelle entstandene **Variante** eines Kapitels mit der **aktuellen Version** im Repo, liefere einen strukturierten Vergleichs-Report und baue auf Autor-Freigabe einen Hybrid ein.

**Findings-Format-Pflicht:** Master = `buch/_findings-format.md`. Council-Subagenten und Verifikations-Council geben Findings im Block-Format mit Vorher/Nachher und Satz-Kontext aus, Tags `[PFLICHT]`/`[TIC]`/`[STIL?]`. Hybrid-Einbau-Findings als Tabelle | alt | neu | warum |.

**Zweck:** Wenn der Autor ein Kapitel an anderer Stelle neu hat schreiben lassen, soll keine der beiden Fassungen blind gewinnen. Der Skill bewertet beide gegeneinander, zeigt was die Variante gewinnt und was sie verloren hat, und empfiehlt einen Hybrid nach dem festen REIN/RAUS-Filter (siehe unten).

**Modell:** Opus (Hauptsession). Council-Subagenten und Verifikations-Council: Opus (keine Modell-Checks, Memory `feedback_nur_opus`).

## Input

`$ARGUMENTS` = Kapitel-ID + Varianten-Prosa.

- Kapitel-ID im neuen Format: `B1-K22`, `K22`, oder Dateiname.
- Die **Varianten-Prosa** wird direkt nach dem Aufruf mitgeschickt (im selben Block oder in der Folgenachricht).
- Optional: eine **kapitelspezifische Canon-Risiken-Liste** (z.B. „K22 sagt noch ›pro Stunde‹"). Wenn nicht mitgeliefert, zieht der Skill nur die Standard-Memory-Fallen.

Wenn keine Kapitel-ID: fragen. Wenn keine Variante: fragen und warten.

## Phase 0 — Guard-Checks

### 0.1 Kapitel-Datei existiert?

`buch/kapitel/B1-K{NN}-{figur}.md` vorhanden? Sonst: Liste aus `ls buch/kapitel/B1-K{NN}*` zeigen und fragen.

### 0.2 Temp-File-Check

Wenn `buch/kapitel/_tmp_B1-K{NN}-variante.md` schon existiert: prüfen ob inhaltsgleich mit der mitgeschickten Variante. Bei Abweichung NICHT still überschreiben — Autor fragen.

### 0.3 Status-Check

Aus `status.json` lesen. `/alternative` arbeitet auf **finalen** Kapiteln (oder `entwurf-ok`/`ausarbeitung` falls der Autor explizit eine Variante eines Entwurfs vergleichen will — dann ist die „aktuelle Version" der Entwurf, nicht das finale Kapitel). Bei `idee`/`entwurf`: warnen, dass es noch keine belastbare „aktuelle Version" gibt.

## Phase 1 — Variante speichern

Variante als `buch/kapitel/_tmp_B1-K{NN}-variante.md` schreiben, mit Kennzeichnungs-Header in Zeile 1:

```
# B1-K{NN} — {Figur} (VARIANTE {ISO-Datum})
```

## Phase 2 — Council parallel

Zwei `Agent`-Calls in **EINEM** Tool-Call, parallel — je ein vollständiger 3-Reviewer-Council:

- **Agent A:** Council auf `buch/kapitel/B1-K{NN}-{figur}.md` (aktuelle Version)
- **Agent B:** Council auf `buch/kapitel/_tmp_B1-K{NN}-variante.md` (Variante)

Jeder Agent liest in dieser Reihenfolge: `buch/00-positioning.md` ZUERST, dann die Zieldatei, `buch/02-stilregeln-v2.md`, `buch/01-autorin-stimme.md`, das chronologisch vorherige finale Kapitel (für Konsistenz/Cross-POV).

**Drei Reviewer pro Agent** (sequenziell, jeder sieht die vorherige Kritik):
1. **Romantasy-Leserin** — Sog, Emotion, Tension, Withholding. Prüft gegen SenLinYu/Yarros/Maas. Plus Pflicht-Lob-Tabelle (≥5 starke Stellen).
2. **Strukturanalyst** — Pacing, Tschechow, Logikfehler, Konsistenz mit Nachbar-Kapitel, Cross-POV-Doppelungen, Premature Doubt, Sorel-Prinzip.
3. **Stilkritiker** — Stilregeln aus `02-stilregeln-v2.md`: keine Em-Dashes, „Takt" nur Uhr/Werk, „Puls" → Körperstelle, „halb X"/„nicht X sondern Y" Pflicht-Prüfung, keine benannten Emotionen, Verb-/Adjektiv-Präzision, keine kryptischen Meta-Kommentare, Verständlichkeits-Gate.

**Output pro Agent:** Score pro Achse, Gesamtverdikt (%/10, BESTANDEN/NICHT BESTANDEN), **Stärken-Profil** (welche Absätze/Beats sind die Kronjuwelen — präzise, für den Hybrid-Vergleich) und **Schwächen-Profil** (was zieht runter / was fehlt / was ist zu dünn).

## Phase 3 — Wortzahl & Tiefer-Diff

`wc -w` auf beide Dateien. Differenz in % berechnen.

**Bei >10 % Wortzahl-Differenz: Tiefer-Diff PFLICHT.** Die Hauptsession vergleicht beide Texte beat-für-beat und listet:
- Was die kürzere Version **gestrichen oder verändert** hat.
- Pro Schnitt ein Urteil gegen den REIN/RAUS-Filter: **trägt der Schnitt** (✅ RAUS-konform) oder ist er ein **Verlust** (❌ REIN-Pflicht: Plot-Beat, Charakter-Beat, Gut-Punch, Dialog mit Inhalt, Tschechow-Setup, Wissensstand-Marker)?

## Phase 4 — Vergleichs-Report

Ausgabe **exakt nach diesem Template** (Markdown-Tabellen, kein Fließtext-Brei):

```
# /alternative — Vergleich B1-K{NN}: AKTUELL vs. VARIANTE

Kapitel:     B1-K{NN} ({POV-Figur}) · {Datum-Header}
Wortzahl:    Aktuell {N} W · Variante {M} W · Differenz {±X %}
Tiefer-Diff: {ja — >10% / nein}

## Council-Scores

| Achse                                          | Aktuell          | Variante         |
|------------------------------------------------|------------------|------------------|
| GESAMT                                         | {8,4 / n. best.} | {7,8 / n. best.} |
| Sog / Romantasy-Leserin                        | {7}              | {8}              |
| Plot- & Charakter-Vollständigkeit              | {9}              | {7}              |
| Stil-Disziplin (Em-Dash/Takt/Puls/halb/nicht-X)| {7}              | {9}              |
| POV-Schärfe / Berufslinse                      | {8}              | {8}              |
| Heat / Ton-Referenz-Tauglichkeit               | {9}              | {6}              |
| Verständlichkeit / keine Verquastung           | {7}              | {8}              |
| Tschechow / Cross-Kapitel-Anker                | {8}              | {8}              |

## Was die VARIANTE gewinnt

| Bereich           | Aktuell              | Variante               | Filter            |
|-------------------|----------------------|------------------------|-------------------|
| {Bereich}         | {alt}                | {neu}                  | REIN — {Grund}    |

## Was die AKTUELLE Version gewinnt (Verluste in der Variante)

| Bereich         | Aktuell               | Variante                | Urteil                       |
|-----------------|-----------------------|-------------------------|------------------------------|
| {Bereich}       | {alt}                 | {fehlt / gestaucht}     | ❌ {RAUS-Fehler / Beat-Verlust}|

## Tiefer-Diff   (nur bei >10% Wortzahl-Differenz)

| In der Variante gestrichen/verändert | Trägt der Schnitt?            |
|--------------------------------------|-------------------------------|
| {Beat}                               | ✅ ja — {Grund} / ❌ nein — REIN|

## Geteilte Probleme   (BEIDE Versionen — unabhängig vom Hybrid zu fixen)

1. {Canon-Bug / Stilverstoß} — {welche Quelle führt}

## Canon- & Memory-Fallen-Check

| Falle                                  | Aktuell      | Variante     |
|----------------------------------------|--------------|--------------|
| Em-Dashes (Prosa)                      | {0}          | {0}          |
| „Takt" nur Uhr/Werk                    | {ok}         | {Verstoß Z.X}|
| „Puls" → Körperstelle                  | {ok}         | {ok}         |
| Schemen/Resonanz/Quelle nicht in Prosa | {ok}         | {ok}         |
| Sorel-Prinzip / Premature Doubt        | {ok}         | {Wackler Z.X}|
| Cross-POV-Vokabular-Trennung           | {ok}         | {ok}         |
| {kapitelspezifische Canon-Risiken}     | ...          | ...          |

## EMPFEHLUNG

Basis:       {Aktuelle Version / Variante}
Begründung:  {1–2 Sätze}

Aus der {anderen Version} übernehmen (REIN-Filter):
  1. {Import 1 — konkret, alt → neu}
  2. {Import 2}

Nicht übernehmen (RAUS-Filter): {kurze Liste}

Danach zu fixen (Council-Findings der Basis): {PFLICHT/TIC-Liste}

→ FREIGABE? Bei „ok" baue ich den Hybrid ein, lasse einen
  Verifikations-Council laufen (Ziel 9+/10) und committe/deploye.
```

**Ehrlichkeits-Pflicht:** Wenn die Variante klar schwächer ist, NICHT künstlich einen 50/50-Hybrid konstruieren. Dann ist die Empfehlung: aktuelle Version als Basis behalten, nur die wenigen echten REIN-Kandidaten übernehmen, und der Schwerpunkt liegt auf den Council-Findings der Basis. Umgekehrt genauso.

## Phase 5 — GATE

Dem Autor Report + Empfehlung zeigen. **Keine Weiterarbeit ohne explizite Freigabe.** Bei offenen Entscheidungen (z.B. Canon-Frage, Basis-Wahl) `AskUserQuestion` mit konkreten Optionen + Begründung pro Option.

## Phase 6 — Hybrid einbauen

Bei Freigabe, in dieser Reihenfolge:
1. **REIN-Importe** aus der anderen Version (per Edit-Tool).
2. **Council-PFLICHT-Findings** der Basis-Version.
3. **Council-TIC/STIL-Findings** der Basis-Version.
4. **Geteilte Probleme** (beide Versionen betroffen).

Alle Änderungen vorab als Tabelle | alt | neu | warum | zeigen (Memory `feedback_findings_alt_neu_tabelle`). Bei größeren Eingriffen blockweise vorgehen, nicht am Stück (Memory `feedback_ausarbeitung_blockweise`).

## Phase 7 — Verifikations-Council

Ein `Agent`-Call (Opus): prüft jeden eingearbeiteten Fix einzeln (sauber JA/NEIN), sucht nach NEU eingeführten Problemen durch die Edits, prüft gegen Stilregeln + Memory-Fallen, vergibt Score %/10.

**Final-Schwelle: 9+/10** (Memory `feedback_final_niveau_9_aufwaerts`). Bei <9: verbleibende PFLICHT-Fixes mit Vorher/Nachher zurückgeben, Fix-Loop, erneute Verifikation. Plateau-Detection: nach 3 Loops ohne 9+ Autor entscheiden lassen.

## Phase 8 — Commit & Deploy

- `wc -w` neu, falls das Kapitel im `status.json` ein `woerter`-Feld trägt: aktualisieren.
- **Nur die Kapitel-Datei** stagen (`git add buch/kapitel/B1-K{NN}-{figur}.md` [+ ggf. `status.json`]). Andere modifizierte/untracked Files NICHT mit einsammeln.
- Commit-Message: `polish(B1-K{NN}): Varianten-Hybrid + Council-Fixes` plus Kurzbeschreibung der Importe und Fixes. Co-Authored-By-Zeile.
- Push (Hook deployed automatisch).
- **Temp-Files:** `_tmp_B1-K{NN}-variante.md` (und ggf. `-alt.md`) NICHT eigenmächtig löschen — Autor fragen, ob sie als Referenz bleiben oder weg sollen.

## REIN/RAUS-Filter (feste Autor-Vorgabe)

**REIN — beim Hybrid übernehmen:**
- Plot-Beats (was passiert, wer entscheidet was)
- Charakter-Beats (Selbst-Erkenntnis, Mikro-Tells, Berufslinsen-Marker)
- Cross-Kapitel-Anker (Tidemoor-Spuren, Anker-Stunde, Vier-Resonanzen, Tschechow-Token)
- Dialoge mit Inhalt
- Tschechow-Setup für spätere Kapitel
- Wissensstand-Marker (wer weiß was)
- Stilistische Verbesserungen der jeweils anderen Version (Em-Dashes raus, weniger Aphorismen, weniger Negationen-Cluster, weniger Stakkato-Kaskaden)

**RAUS — nicht übernehmen:**
- Atmosphäre-Doppelungen
- Aphorismen ohne Beat-Boden (Wurzeln/Türen/etc.)
- Filler-Dialog ohne Inhalt
- Bürokratie-Details ohne Plot
- Frage-Antwort-Spiele, die eine straffe Variante zerschneiden
- King-Detail-Stapelung ohne echte Tschechow-Funktion

## Memory-Fallen-Check (Standard, immer prüfen)

- „Schemen" / „Resonanz" / „Quelle" als Phänomen-Begriff nicht in Prosa
- Em-Dashes (—) in der Prosa verboten (Header-Em-Dash im Kapiteltitel ist erlaubt)
- „Takt" nur auf Uhr/Werk, nicht auf Brust/Atem/Stein
- „Puls" durch Körperstelle ersetzen (Quellenpuls als Canon-Begriff ausgenommen)
- „halb X" und „nicht X, sondern Y" — Pflicht-Prüfung pro Einsatz, Default streichen
- Keine Erden-Wissenschaftler-Namen (Newton/Einstein etc.)
- „Sauber" als Bewertung verboten (Epoche 1820), keine Anglizismen
- Areligiös — keine Tempel/Priester/Götter-Reflexe
- Magie hat keine Kosten — keine Erschöpfungs-Beats
- Cross-POV-Vokabular-Trennung (Alphina=Nebel, Sorel=Dunst, Maren=Werftsalz/Meerluft, Vesper=Schlag/Takt-Werk)
- Sorel-Prinzip: Erzähler weiß nie mehr als die POV-Figur; kein Premature Doubt
- Keine eigenmächtigen Plot-Additionen — bei Canon-Lücken fragen

## Regeln

- **Kein Einbau ohne Freigabe.** Phase 5 ist ein hartes Gate.
- **Ehrliche Empfehlung.** Wenn eine Version klar gewinnt, das sagen — keinen Hybrid erzwingen.
- **Variante als Backup behalten** bis der Autor anders entscheidet.
- **Nur die Kapitel-Datei committen** — keine fremden Änderungen mitnehmen.
- **Final erst bei 9+/10** durch Verifikations-Council.
- Deutsch, Umlaute in der Zielprosa (ä/ö/ü/ß), kein ae/oe/ue.

## Gates (Zusammenfassung)

| Gate                  | Bedingung                                             |
|-----------------------|-------------------------------------------------------|
| Kapitel-Datei + Variante vorhanden | Sonst fragen                             |
| Temp-File-Überschreiben | Bei Abweichung Autor fragen                         |
| Vergleichs-Report freigegeben | Explizites Autor-„ok" vor Phase 6           |
| Verifikations-Council 9+/10 | Vor Commit                                    |
| Temp-File-Löschung    | Nur nach Autor-Entscheidung                           |

$ARGUMENTS
