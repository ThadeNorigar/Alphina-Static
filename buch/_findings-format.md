# Findings-Format — Pflicht-Spec für alle Skills und Subagenten

Jedes Finding (Stil-Befund, Konsistenz-Bug, Council-Vorschlag, Genre-Leserin-Note, Refit-Empfehlung, Lektorat-Mikro-Fix, Logik-Hinweis, Figuren-Check) wird im **Block-Format mit Vorher/Nachher und Satz-Kontext** ausgegeben — niemals als verkürzte Tabellen-Zeile, niemals als reine Wort-zu-Wort-Substitution.

**Hintergrund (Memory `feedback_findings_mit_kontext.md`, `feedback_findings_alt_neu_tabelle.md`):** Reine Wort-Aenderungen ohne Kontext sind unbrauchbar — Aphorismen, Stakkato und Hedges tragen nur im umgebenden Beat. Der Autor muss die Aenderung im Satz-Umfeld pruefen koennen. Verkuerzte Synthese-Tabellen (»Was raus« / »Vorschlag«) verbieten sich, weil sie genau diese Beurteilung verhindern.

## Pflicht-Block-Format

```
### {ID} — Z.{NN} [{TAG}]

**vorher:**
> {1 Satz davor — damit die Stelle einordbar ist}
> {betroffene Stelle}
> {1 Satz danach}

**nachher:**
> {1 Satz davor — unveraendert}
> {neue Stelle / [STREICHEN]}
> {1 Satz danach — unveraendert}

**warum:** {1 Satz mit Master-Verweis falls einschlaegig}
```

**ID-Schema:**
- Subagent-Findings: `A01`, `B01`, `C01`, ... (Subagent + Nummer)
- Synthese-Master-Tabelle: gleiche IDs, unverändert übernommen
- Council-Findings: `LINA-01`, `MEIKE-01`, `VICTORIA-01`, `KAYA-01`, `NORA-01` (Stimme + Nummer)
- Logik/Konsistenz: `LOG-01`, `KON-01`
- Lektorat-Mikro: `LEK-01`

**Tag-Schema (verbindlich):**
- `[PFLICHT]` — Konsistenz-/Canon-/Magie-/POV-Bug ODER klare Stilregel-Verletzung ohne Funktion. Wird ohne Diskussion gefixt.
- `[TIC]` — austauschbare/leere Konstruktion ohne Funktion (Default-Verb-Tic, Aphorismus ohne Beat, mechanische Negation, Substantiv-Phrase ohne Verb). Default fixen, Autor kann widersprechen.
- `[STIL?]` — formale Regelverletzung, aber Funktion erkennbar (Welt-Beat, Charakter-Beat, Pacing-Pflicht, Aftermath, Erinnerungs-Inventar). Default behalten, Autor entscheidet.

## Funktional-Filter (PFLICHT vor jedem Tag)

Vor jeder Vergabe von `[PFLICHT]` oder `[TIC]` durchläuft der Subagent vier Fragen:

1. **Welt-Beat?** Trägt die Stelle einen Welt-Zahn (atmosphärische Drohung, Setting-Detail mit Konsequenz, Tschechow-Setup)?
2. **Charakter-Beat?** Selbstkorrektur, innerer Bruch, Verdrängungs-Geste, Wahrnehmungsgrenze?
3. **Pacing-Pflicht?** Erfüllt die Stelle eine Stilregel-Pflicht (Aftermath nach Climax, Erinnerungs-Inventar, Rhythmus-Gegenpol)?
4. **Streichen-Test:** Wäre die Prosa nach dem Streichen schwächer als jetzt?

Wenn 1× ja → `[STIL?]` statt `[PFLICHT]`/`[TIC]`, und die Funktion in „warum" benennen.

**Aphorismen, Stakkato, „wie X"-Vergleiche, Antithesen, Negationen sind nicht per se verboten** — sie sind verboten als **Tic** (uninspiriert, austauschbar, leer). Wenn elegant + sinnvoll gesetzt, sind sie Stilmittel und tragen das `[STIL?]`-Tag, nicht `[TIC]`/`[PFLICHT]`.

## Synthese-Master-Tabelle (in Hauptsession nach Subagent-Lauf)

Die Hauptsession konsolidiert die Subagent-Findings in **drei Blöcken**, jeweils im selben Block-Format:

- **Block A — PFLICHT** (Konsistenz/Canon-Verstoss + klare Stilregel-Verletzungen ohne Funktion) — wird ohne Diskussion gefixt
- **Block B — EMPFEHLUNG** (klarer Stil-Tic, keine Funktion) — Default fixen
- **Block C — STIL-VORBEHALT** (formal Verstoss, Funktion da) — Default behalten, Autor entscheidet

Innerhalb jedes Blocks: jedes Finding als voller Vorher/Nachher-Block mit Kontext. Kein Kürzen auf Mini-Tabelle. Bei mehreren Subagenten-Stimmen zur selben Zeile: Stimmen in der „warum"-Zeile aggregieren („A03 + B01 — Selbstkommentar + leeres Verb").

## Sweep-Aenderungen

Bei wiederholter Mikro-Aenderung (z.B. „Nebel → Dunst" 9× in einem Kapitel) reicht **ein Block mit 2-3 typischen Beispielen** plus Hinweis „identisch an Z.X, Y, Z, ...". Kein Pflicht-Block pro Vorkommen, aber mindestens drei Beispiele mit Kontext.

## Knapp-Original-Default

Wenn der Original-Satz unter 8 Woertern ist und einen klaren Beat trägt (Aphorismus, Pointe, Hammerschlag, Vergleich), Default-Empfehlung ist **BEHALTEN**. Erweiterungen oder Aufloesungen nur, wenn ein Subagent klaren Tic-Charakter (austauschbar, leer, semantisch redundant) belegt. Kurze elegante Saetze nicht „verbessern".

## Welt-Kanon-Verstaendlichkeits-Test

Wenn ein vorgeschlagener Fix einen Welt-Kanon-Eigennamen oder Spezialterm in die Prosa einfuehrt (z.B. „Solm", „Quellpuls", „Resonanz"), pruefen ob die Stelle ohne Erklaerung verstaendlich ist. Default = generisch bleiben („Muenze", „Schmerz", „Wachstum") statt erfinden. Erfundene Begriffe nur wenn etablierter Canon UND in vorherigen Kapiteln schon mehrfach erschienen.

## Quellen-Vergleich (Leseproben, Refit, Ausarbeitung)

Wenn eine Probe oder ein Kapitel gegen eine externe Referenz (`buch/referenzen/Leseprobe RY.txt`, `Leseprobe JM.txt`, `Leseprobe SLY.txt`, `Leseprobe Reage.txt` + zugehoerige `*-stil-analyse.md`) verglichen wird, gilt **asymmetrische Kritik**: die Probe ist die Schuelerin, die Quelle ist die Lehrerin.

**Verboten:**
- „Was die Probe BESSER macht als die Quelle"-Tabellen — Selbstbestaetigung, kein Lerneffekt
- Symmetrischer Vergleich „beide haben Vor- und Nachteile" — verschleiert das Delta
- Wohlwollende Begruendungen, warum das Eigene gleichwertig sei (knapper, subtiler, dichter…)

**Pflicht:**
- **Tabelle „Was die Quelle besser macht als wir"** mit konkreten Hebeln, Quell-Zitat, eigenem Defizit, Lerneffekt. Mindestens 5-8 Hebel pro Vergleich.
- **Übernahme-Liste:** pro starkem Hebel ein konkreter Übernahme-Vorschlag fuer die Probe — was waere die Mikro-Aenderung, die den Hebel an unserem Material aktiviert?
- **Was wir bewusst NICHT übernehmen**, weil es nicht zu unserem Canon/Setting/POV passt — auch das gehört in den Vergleich (z.B. Yarros 1. Pers, RY-Snark passt nicht zu Alphinas Kontroll-Stimme). Begruendung pro Verzicht.

**Was die Probe stark macht** ist NICHT Teil des Quellen-Vergleichs — das gehoert in die Pflicht-Lob-Tabelle (Genre-Leserin / Council). Diese Trennung ist hart: Lob-Tabelle = was funktioniert in der Probe selbst. Quellen-Vergleich = was die Quelle uns voraus hat.

**Format der „Was die Quelle besser macht"-Tabelle:**

| Hebel | Quelle (Z.) | Quell-Zitat | Probe-Defizit | Übernahme |
|---|---|---|---|---|
| z.B. „Welt greift mehrfach ein" | RY Z.34 | „die Temperatur im Raum abrupt abfällt" | nur 2 Welt-Eingriffe (Kutsche, Hammer) | zusätzliche Welt-Reaktion in Mitte einbauen |

## Pflicht-Lob-Tabelle (Genre-Leserin-Subagenten + Council)

Genre-Leserin-Stimmen (LINA/NORA/MEIKE/VICTORIA/KAYA) und Council-Stimmen müssen zusätzlich zur Findings-Liste eine **Lob-Tabelle** liefern: mindestens 5 Stellen, die explizit funktionieren. Format:

| Z. | Stelle | warum stark |
|---|---|---|

Die Hauptsession nutzt das, um Subagent-1-/Subagent-2-Findings zu kontern: was eine Stimme als Tic markiert, kann eine andere als starken Beat loben — dann wandert das Finding automatisch in Block C.

## Verbotene Output-Formen

- **Kein** „Was raus → Vorschlag"-Mini-Tabelle ohne Vorher/Nachher mit Kontext
- **Keine** reine Wort-zu-Wort-Substitution (z.B. „ärgerte sie" → „[STREICHEN]") ohne den Satz davor und danach
- **Keine** Aufzählung von Findings ohne Block-Struktur
- **Keine** „warum"-Zeile, die nur „Stilregel-Verstoss" sagt — immer den Master-Bezug nennen (z.B. „Master `01-autorin-stimme.md` §8 Scharnier-Aphorismen")

## Anwendung in Skills

Diese Spec ist **verbindlich** für:

- `/refit` (Phase B3 — Konsolidierung) — Inline-Definition zusätzlich, hier kanonisch
- `/ausarbeitung` (Phase 2 — Master-Tabelle nach Subagenten-Lauf) — Inline-Definition zusätzlich, hier kanonisch
- `/stil-check` — Findings-Liste
- `/council` — pro Agent eine Findings-Liste + Synthese
- `/book-council` — pro Leserinnen-Archetyp eine Findings-Liste + Synthese
- `/lektorat-fix` — Mikro-Fixes mit Kontext (Sweep-Format erlaubt)
- `/lektorat-online` — Online-Kommentare mit Vorher/Nachher
- `/figuren-check` — Konsistenz-Findings
- `/logik-check` — Logik-/POV-Findings
- `/entwurf` (Phase Council-Loop) — Findings auf Entwurf
- `/brainstorm` (wenn Findings auftreten)

Subagent-Prompts in allen genannten Skills referenzieren diese Datei statt eigener Format-Definitionen. Aenderungen am Format hier propagieren auf alle Skills automatisch.

## Beispiel — Vollständiges Finding

```
### A03 — Z.43 [PFLICHT]

**vorher:**
> »Nein.«
> Sie atmete durch die Nase aus. Unter den Rippen zog sich etwas zusammen, was sie nicht zugelassen hatte.
> Sie hätte jetzt gehen können.

**nachher:**
> »Nein.«
> Sie atmete durch die Nase aus. Unter den Rippen zog es sich zusammen.
> Sie hätte jetzt gehen können.

**warum:** „was sie nicht zugelassen hatte" ist Selbstkommentar mit leerem Verb (`01-autorin-stimme.md` §8 „Figur redet über sich selbst") plus sinnfreie Negation (`feedback_negationen_vermeiden.md`). Körperbeat allein trägt.
```
