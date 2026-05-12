# /praezision — Satz-Prüfung: Verständlichkeit + Verb-Präzision + Adjektiv-Präzision

Du prüfst ein Kapitel von „Der Riss" satz-für-satz auf drei Achsen: **(1) verständliche deutsche Sprache**, **(2) Verb-Präzision**, **(3) Adjektiv-Präzision**. Bericht im Block-Format, dann Gate, dann auf Freigabe hin Einarbeitung.

Dieser Skill ist **nicht** der grosse `/stil-check`. Keine Rhythmus-/Antithese-/POV-Vokabular-Checks, kein Kontrollverlust-/Begehren-/Geschmacks-Audit. Nur die drei Achsen oben — fokussiert und schnell.

## Findings-Format-Pflicht

Master = `buch/_findings-format.md`. Jedes Finding strikt im Block-Format (Vorher/Nachher mit Satz davor + Stelle + Satz danach), Tag aus `[PFLICHT]` / `[TIC]` / `[STIL?]`, „warum" mit Master-Verweis. Funktional-Filter vor jeder Tag-Vergabe. Sweep-Aenderungen mit 2-3 Beispielen + Hinweis.

## Input

`$ARGUMENTS` = Pfad zur Kapitel-Datei (z.B. `buch/kapitel/B1-K34-alle.md`).

Wenn kein Argument: frage welche Datei.

## Phase 0 — Kontext laden

Lies parallel:
1. **`buch/00-positioning.md`** — Marktposition. Verständlichkeit hat Vorrang vor literary-Knappheit. Commercial Dark Fantasy/Romantasy/BDSM.
2. **Die Kapitel-Datei** ($ARGUMENTS).
3. **`buch/02-stilregeln-v2.md`** — insbesondere die Sektionen „Verb-Präzision: Default-Sein-Verben als Tic", „Verquastungs-Test", „Vollständige Sätze als Default". Schwellen und Beispiele stammen ausschliesslich aus dem Master, nicht aus diesem Skill.
4. **`buch/01-autorin-stimme.md`** — §6.5 (Sinnes-Adjektiv-Pflichtstellen, Label-Verbot).
5. **`buch/_findings-format.md`** — Output-Spec.

Bestimme:
- POV-Figur (Alphina / Sorel / Vesper / Maren / Runa / Nyr / …)
- Wort- und Satzanzahl (grobe Zählung)
- Bei mehreren POVs im Kapitel: pro Szene neu prüfen.

## Phase 1 — Satz-für-Satz-Prüfung (drei Achsen)

Gehe das Kapitel **Absatz für Absatz, Satz für Satz** durch. Pro Satz die drei Achsen anwenden. Findings sammeln, NICHT bewerten — die Konsolidierung läuft in Phase 2.

### Achse A — Verständlichkeit

Pro Satz die folgenden Tests:

**A1 — Mündlicher Lese-Test:**
Mental aussprechen. Würde ein Mensch am Tisch das so sagen, ohne zu stocken? Bei Stockung → FINDING. Insbesondere: Apposition vor Verb, dreifach-verschachtelte Relativ-Sätze, Substantiv-Stapel ohne Verb (siehe Memory `feedback_muendlicher_lesetest.md`, `feedback_vollstaendige_saetze_default.md`).

**A2 — Pronomen-Referenz:**
Jedes `er/sie/es/ihn/ihm/sich` muss eindeutig zuordenbar sein. Im Zweifel: ist nach ein-mal-Lesen klar, wer/was gemeint ist? Wenn nicht → FINDING.

**A3 — 10-Punkt-Verquastungs-Test** (siehe Memory `feedback_verquastung_katalog.md` + Master `02-stilregeln-v2.md` Sektion „Verquastungs-Test"):
- (1) Aussprechen — stockt der Sprecher?
- (2) Pronomen-Check (s. A2)
- (3) Vorgangs-Check — Bild konkret oder abstrakt?
- (4) Verb-Check — trägt das Verb oder ist es leer?
- (5) Logik-Check — folgt der Satz aus der Welt?
- (6) Pseudo-Material — „Nichts"/„Etwas" als Stand-in?
- (7) Holprige Wortstellung?
- (8) Pseudo-Tiefe — klingt klug, sagt nichts?
- (9) Anachronismus (frühes 19. Jhd. — keine Anglizismen, kein „Drift"/„Charge"/„Debugging")?
- (10) Beispielkatalog im Master durchprüfen.

**A4 — Vollständige Sätze:**
Default = Subjekt + Verb. Adjektiv-Anhängsel nach Komma („Tee, dampfend") und Substantiv-Phrasen ohne Verb („Spalten in ihrer Hand.") als eigenständige Sätze sind FINDING — es sei denn, der Beat trägt sie zwingend (Schock, Bruch, Hammerschlag, mit Begründung pro Einsatz, siehe Memory `feedback_vollstaendige_saetze_default.md`, `feedback_kein_stakkato_dialog.md`).

**A5 — Verständlichkeits-Gate:**
Bleibt ein Satz beim ersten Lesen unklar → FINDING, unabhängig davon, wie elegant er ist (Memory `feedback_verstandlichkeits_gate.md`, `feedback_verstandlichkeit_vor_eleganz.md`).

**A7 — Sinnfreie Negationen / Verneinungs-Tic:**
**Pflicht-Prüfung pro Einsatz.** Jede Negation (`nicht / kein / nichts / niemand / nie / weder ... noch`) durchläuft den Streichen-Test: trägt eine **positive Formulierung** dieselbe Information genauso oder besser? Wenn ja → FINDING. Default = streichen oder positiv umformulieren. Memory `feedback_negationen_vermeiden.md`.

Verbotene Tic-Muster (fast immer FINDING):
- *„nicht X, sondern Y"* (Antithese — Master Tabelle „Harte Limits")
- *„nicht X und nicht Y"* (Doppelnegation als Charakter-Label, z.B. *„nicht warm und nicht kalt"*) — sagt nicht, was etwas IST, nur was es nicht ist. Streichen oder positiv: *„blieb sachlich"*.
- *„nicht X, nicht Y"* nach bereits gegebener positiver Info (z.B. *„zwei Schritte weiter in der Gasse, nicht nah, nicht fern"*) — redundant.
- *„kein X. Nur Y."* als Pointe
- *„X, nicht Y"* wenn Y nie behauptet wurde
- *„weiß nicht / kann nicht / konnte nicht"* am Satzende als resignativer Abschluss
- *„Nichts [Verb]te"* / *„Nichts blieb"* als Absatz-Schluss-Hammer
- *„geben + nichts"* (z.B. *„gab ihr nichts"*) — leeres Verb + Pseudo-Material kombiniert

**Erlaubte Negation:** Echte Abwesenheits-Aktion — die Figur verweigert, schweigt, fehlt, kommt nicht. *„Er sagte nichts."* / *„Sie ging nicht."* — der Akt der Abwesenheit ist die Aussage.

Tag: `[PFLICHT]` bei klar redundanter Negation, `[TIC]` bei austauschbarer, `[STIL?]` wenn die Verneinung selbst der Beat ist (Verweigerung, Fehlen, bewusste Abwesenheit).

**A6 — Gedankenstrich-Tic (Em-Dash `—` und Double-Dash `--`):**
**Hartes PFLICHT-Sweep.** Jedes Vorkommen von `—` (Em-Dash, U+2014) und `--` (Doppel-Bindestrich als Gedankenstrich-Ersatz) in der Prosa ist FINDING. Ausnahme: Bindestriche in zusammengesetzten Wörtern (`Hände-Platte`, `Gewebe-an-Gewebe`, `Zwanzig-Sekunden-Belichtung`) bleiben erlaubt — die sind keine Gedankenstriche.

Ersatz pro Funktion:
- **Apposition / Glied-Liste:** Doppelpunkt (`Er sah es: leer.`) oder Komma (`Er sah es, leer.`)
- **Erläuterung / Aufzählung:** Doppelpunkt
- **Zwei gekoppelte Hauptsätze:** Semikolon oder neuer Satz
- **Hammerschlag-Schluss:** neuer Satz (Punkt)
- **Dialog-Abbruch (`dann —`):** Auslassungspunkte (`dann …`)

Sweep-Format bei >5 Vorkommen: ein PFLICHT-Block mit 3-4 Beispielen + Hinweis „identisch an Z.X, Y, Z, …", plus Liste aller Stellen.

Memory: `feedback_keine_gedankenstriche.md`. **Keine Schwelle** — jedes Vorkommen raus.

### Achse B — Verb-Präzision

Pro Satz alle Verben listen. Pflicht-Prüfung pro Einsatz, **keine numerische Schwelle**.

**B1 — Default-Sein-Verben** (`lag/lagen/war/waren/stand/standen/saß/saßen`):
Pro Vorkommen prüfen: trägt das Verb das Bild — oder ersetzt es nur „befand sich"? Wenn das Subjekt **wirklich liegt** (gefallen, horizontal, ruhend) → präzise, kein Finding. Wenn metaphorisch / Position-Stand-in → FINDING, präzises Alternativ-Verb vorschlagen (*steckte, klemmte, hing, ruhte, brannte, dampfte, fiel, sich türmte, lehnte, lastete*).

**Tic-Schwelle Sein-Verben:** dasselbe Sein-Verb >2× im Block → mindestens zwei ersetzen (Memory `feedback_verb_praezision.md`, Master `02-stilregeln-v2.md` „Verb-Präzision").

**B2 — Default-Aktion-Verben** (`machen/gehen/legen/setzen/nehmen/geben/halten/lassen/tragen/schicken/rufen/kommen/tun/haben/werden`):
Pro Vorkommen prüfen: gibt es ein präziseres Alternativ-Verb, das mehr Information trägt? Alternativen aus Memory `feedback_bild_logik_verb_praezision.md`:
- *legen* → ruhen / klemmen / lehnen / stützen / drapieren / streifen
- *gehen* → schreiten / treten / tappen / schleichen / huschen / stapfen
- *machen* → fertigen / brauen / mischen / rühren / hämmern / ziehen
- *halten* → klammern / pressen / klemmen / umfassen / packen / stützen
- *nehmen* → greifen / fassen / pflücken / schnappen / aufnehmen
- *kommen* → eintreten / nähern / erscheinen / auftauchen / erreichen
- *sehen* → mustern / spähen / blinzeln / streifen / fixieren / schweifen
- *hören* → vernehmen / lauschen / horchen / aufhorchen
- *fühlen* → spüren / wittern / ahnen / merken / erschauern

Wenn Default-Verb hier eine echte Funktion hat (Rhythmus, Beat-Pacing, neutrale Vermittlung) → `[STIL?]`, in „warum" die Funktion benennen. Wenn austauschbar → `[TIC]` mit Vorschlag.

**B3 — Personifikation:**
Verben mit menschlicher Aktivität auf nicht-belebten Subjekten (Stadt „schaut", Licht „kriecht", Stille „klemmt", Raum „atmet") — innere Bild-Logik prüfen. Wenn das Bild physikalisch nicht trägt → FINDING. (Memory `feedback_bild_logik_verb_praezision.md`.)

**B4 — Leere Verben** (`schickte / hielt / lenkte / gehörte / fand / fasste`):
Pro Vorkommen prüfen: trägt das Verb einen konkreten Vorgang oder steht es als Pseudo-Aktivität? Beispiele aus Memory `feedback_verquastung_katalog.md`:
- „weil das Licht da war und nicht hingehörte" → leeres „gehören"
- „Was die Flamme an den Tisch schickte" → leeres „schicken"
- „hielt seinen Willen auf einen Punkt" → leeres „halten"

### Achse C — Adjektiv-Präzision

Pro Satz alle Adjektive listen. Pflicht-Prüfung pro Einsatz, **keine numerische Schwelle** (siehe Memory `feedback_adjektiv_praezision.md`).

**C1 — Bild-Boden:**
Kann eine Handwerkerin / Botanikerin / Uhrmacherin das Adjektiv am bezeichneten Objekt **körperlich verifizieren**? (Stein „kalt" — ja, fühlbar. Stein „taub" — nein, Personifikation.) Wenn nein → FINDING.

**C2 — Personifikations-Adjektive** (`taub / stumm / blind / schlafend / wach`):
Auf nicht-belebten Objekten fast immer FINDING. Ausnahme: das Bild trägt explizit eine Sinnes-Übertragung mit physikalischem Boden. Beispiele:
- *„der Stein blieb für sie taub"* → FINDING (Stein hat kein Gehör). Fix: *„der Stein gab unter ihren Händen nicht nach"*.
- *„Wohin sie kamen, blieb stumm"* → FINDING (ein Ort kann nicht stumm sein). Fix: *„Wohin sie kamen, hat niemand erfahren"*.

**C3 — Universelle Label-Adjektive** (`still / leer / dicht / eng / weit / kalt / warm / schwer / leicht / fern / klar / dunkel / hell / scharf / weich / hart / ruhig / sanft`):
Pro Einsatz prüfen: trägt das Adjektiv konkret das Bild oder ist es Stimmungs-Sprache? Bei Stimmungs-Einsatz → FINDING; ersetzen durch konkretes Sinnes-Adjektiv aus dem Material-Register (salzig / harzig / kalkig / ledern / ölig / kupfern / leinen) oder durch Handlung/Material.

**C4 — Label-Adjektive aus Autorin-Stimme §6.5** (`verspielt / wollüstig / ernsthaft / nüchtern / sanft / zärtlich / liebevoll / leidenschaftlich / hingerissen / bedrohlich / unheimlich`):
**0 pro Kapitel.** Jeder Treffer ist hartes FINDING. Test: Würde ein präziseres Verb oder ein Körperbeat das Adjektiv ersetzen? Wenn ja: Adjektiv streichen, Beat einsetzen. Ausnahme: in Dialog-Repliken, wo die Figur das Wort **selbst** sagt.

**C5 — Adjektiv-Wiederholung — Hartregel:**
**Maximal 2× pro Block.** Drittes Vorkommen → automatisch **PFLICHT-FINDING** „Adjektiv-Wiederholung" (nicht TIC, kein STIL?). So viele ersetzen, dass die Schwelle wieder unter 3 fällt. Gilt auch kapitelweit, wenn dasselbe Adjektiv hörbar wiederkehrt (z.B. *ruhig* 7× verteilt). Memory `feedback_adjektiv_praezision.md`.

## Phase 2 — Konsolidierung & Bericht

Alle Findings in den Master-Tabelle-Format aus `buch/_findings-format.md` konsolidieren. **Drei Blöcke:**

- **Block A — PFLICHT:** klare Verständlichkeits-Brüche (Pronomen-Verwirrung, Verquastung, Hae?-Sätze), Personifikations-Adjektive ohne Bild-Boden, Label-Adjektive aus §6.5 → ohne Diskussion fixen.
- **Block B — EMPFEHLUNG (TIC):** Default-Verb-Tic, Default-Adjektiv-Tic, Adjektiv-Wiederholung ohne Funktion → Default fixen.
- **Block C — STIL-VORBEHALT:** formale Regelverletzung mit erkennbarer Funktion (Welt-Beat / Charakter-Beat / Pacing-Pflicht) → Default behalten, Autor entscheidet.

Pro Finding: voller Vorher/Nachher-Block mit Satz davor + Stelle + Satz danach. Keine verkürzten Tabellen. Sweep-Format (2-3 Beispiele + Hinweis) bei wiederholtem Mikro-Pattern.

### Bericht-Header

```
## Präzisions-Check: [Dateiname]
POV: [Figur(en)] | Wörter: [N] | Sätze: [N]

### Übersicht
| Achse | Findings PFLICHT | TIC | STIL? |
|-------|------------------|-----|-------|
| A — Verständlichkeit | N | N | N |
| B — Verb-Präzision   | N | N | N |
| C — Adjektiv-Präzision | N | N | N |
| Summe | N | N | N |
```

### Findings-Blöcke

`### Block A — PFLICHT` → alle PFLICHT-Findings im Vorher/Nachher-Format.
`### Block B — EMPFEHLUNG` → alle TIC-Findings im Vorher/Nachher-Format.
`### Block C — STIL-VORBEHALT` → alle STIL?-Findings im Vorher/Nachher-Format.

### Sauber

Kurze Liste (3-5 Punkte): was an Verb-/Adjektiv-Wahl und Satzbau gut funktioniert.

### Verdikt

`9+/10` — Final-fähig wenn Block A leer und Block B <5 Findings.
`7-8/10` — Phase-7-Arbeit, Findings einarbeiten.
`<7/10` — Substanzielle Überarbeitung nötig.

## Phase 3 — Gate

**NACH DEM BERICHT** fragen: *„Bericht gelesen? Soll ich Block A (PFLICHT) und Block B (TIC) einarbeiten? Welche Findings aus Block C willst du übernehmen, welche streichen?"*

Keine Edits ohne explizite Freigabe.

## Phase 4 — Einarbeitung (nur nach Freigabe)

Nach Autor-Freigabe:
1. Alle Block-A-Findings übernehmen (`Edit`-Tool, ein Edit pro Finding-ID).
2. Alle Block-B-Findings übernehmen, **ausser** der Autor hat einzelne explizit gestrichen.
3. Block-C-Findings nur übernehmen, wenn der Autor sie freigegeben hat.
4. Nach jedem Edit kurz prüfen: hat sich das umgebende Satz-Gefüge verschoben? Wenn ja: Folge-Sätze auf Pronomen-Bezug nachprüfen.
5. Am Ende: ein-Zeilen-Diff-Zusammenfassung („N Fixes eingearbeitet, M übersprungen, K offen").

## Regeln

- **Jeden Satz prüfen.** Nicht überfliegen.
- **Pflicht-Prüfung pro Einsatz**, keine Quoten — pro Verb/Adjektiv eine bewusste Entscheidung.
- **Bild-Logik vor Eleganz.** Wenn das Bild im Detail nicht trägt → FINDING, auch bei poetisch klingender Stelle.
- **Verständlichkeit vor Eleganz.** Wenn ein Satz „hae?" produziert → FINDING.
- **Keine Fixes ohne Freigabe.** Nur Bericht in Phase 1-3.
- **Master gewinnt.** Wenn Skill und `02-stilregeln-v2.md` divergieren → Master.

$ARGUMENTS
