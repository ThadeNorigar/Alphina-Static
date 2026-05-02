# Entwurfs-Qualität — Wiederkehrende Findings & Auto-Checks

**Stand:** 2026-05-02
**Quellen:** Memory-Files (`feedback_*.md`, `project_*.md`), Git-Log auf `buch/kapitel/*-entwurf.md`, Archiv-Diskussionen, Skill `.claude/commands/entwurf.md`. Erstellt durch Recherche-Subagent nach B1-K30-Session als Datengrundlage.

**Zweck:** Datengrundlage für `scripts/entwurfs-check.py` (auto-prüfbar) und den Canon-Wächter-Subagent in `/entwurf` Phase 5. Dokumentiert die wiederkehrenden Korrektur-Patterns aus dem Feedback-Loop zwischen `entwurf-checked` und `entwurf-ok`.

---

## Findings-Tabelle (sortiert nach Klasse, dann Häufigkeit)

⚡ = in MEMORY.md mit Prioritätssignal markiert. Häufigkeit: subjektiv aus Git-Log + Memory-Vorkommen.

### Canon (Welt/Figuren/Magie-Konsistenz)

| Finding | Beispiel | Quelle | Häufigkeit | Auto-prüfbar? |
|---|---|---|---|---|
| Sorel-Prinzip / Premature Doubt — Figur weiß mehr als POV erlaubt | K30: Schicksal von Elke/Kesper sollte nicht aus Lenes Manuskript bekannt sein | `feedback_canon_kette_pruefen` | ⚡ sehr häufig | teils (Memory-Abgleich-Subagent) |
| Realweltliche Monatsnamen | K24: „Frühsommer" → „später Frühling (Blütenmond)" | `project_welt_monate_pflanzen` | ⚡ sehr häufig | **ja** (regex) |
| „Moragh" in Thalassien-Kapiteln | K24: Lenes Text nannte „Moragh" als Ortsnamen | `feedback_moragh_name` | ⚡ häufig | **ja** (regex + POV-Check) |
| Spukgeschichte — Passiv-Effekte ohne Urheberin (ab K21 Bruch) | K24 Sz1: Kerze flackert, Folianten rutschen | `feedback_keine_spukgeschichte` | häufig | nein (narrativer Kontext) |
| Fraktionsnamen falsch (Gilden/Binder statt Bund/Velmar) | „die Gilden" statt „der Bund" | `feedback_fraktionsnamen` | mittel | **ja** (regex) |
| „Resonanz" als Begriff in Prosa/Dialog | K23: Sorel sagt „Drei Resonanzen" | `feedback_resonanz_nicht_benennen` | mittel | **ja** (grep `Resonanz` in Prosa-Blöcken) |
| Magie-Kosten / Erschöpfungs-Beats (Thalassier zahlen nicht) | „sie sank zurück, erschöpft" nach Magie | `feedback_kein_magie_kosten` | mittel | teils (grep-Hinweise) |
| Welt-Kleidung — anachronistische Begriffe (Jacke/Bluse) | „Jackentasche" in Entwurfs-Beats | `feedback_kleidung_kanon` | mittel | **ja** (regex) |
| Figurenwissen inkonsistent mit Vorkapiteln | „Maren wohnt nicht im Anker", „Vesper kennt ihn nicht" | `feedback_canon_kette_pruefen` | häufig | teils (Wissensstand-Subagent) |
| Metrische Maßeinheiten (cm, km, Meter) | „300 Meter", „vier Kilometer" | Skill `entwurf.md` §Welt-Konsistenz | mittel | **ja** (regex) |
| Schemen-Magie-Modus undefiniert / Berührungs-Aura statt aktive Magie | K30 (orig): „Knochen-Kälte durch Berührung" ohne Mechanismus | `project_schemen_magie_modi` | neu (B1-K30) | teils (Subagent prüft Mechanik-Definition) |
| Schemen-Lautlosigkeit nicht markiert | K30 (orig): „Klacken auf Pflaster" / „Gelenk knackt" | `project_schemen_magie_modi` | neu (B1-K30) | teils (grep `klack|knack` in Schemen-Kontext) |
| Figuren-Aufstellungen falsch (Runa als „Fünfte") | K30 (orig): „die Fünf" vor Portal-Durchgang | `project_b2_k01-k27_canon` (Runa-Lore) | neu (B1-K30) | teils (Canon-Wächter-Frage) |
| Du/Sie-Konsistenz (ab K22 Du, K19 alle vier per du) | „Sie" zwischen Vier in K23+ | `project_du_sie_wechsel` | mittel | teils (Pronomen-Counter pro Paar) |
| Zwei-Monde-Fehler (Moragh-Regel auf Thalassien) | „zwei Monde am Himmel" in B1 | `project_zwei_monde_moragh` | selten | **ja** (regex in Thalassien-Kapiteln) |

### Sprache (Stil-Tics in Entwurfs-Prosa-Blöcken)

| Finding | Beispiel | Quelle | Häufigkeit | Auto-prüfbar? |
|---|---|---|---|---|
| „nicht X, sondern Y" Häufung | K23 / K30: „kein Versprechen, sondern eine Tatsache" | `feedback_nicht_sondern_pflichtpruefung` | ⚡ häufig | **ja** (regex) |
| Sinnfreie Verneinungen / Negations-Ketten | K24: „Nichts blieb" / „Was aus ihnen wurde, weiß ich nicht" | `feedback_negationen_vermeiden` | ⚡ häufig | teils (Negations-Dichte/Absatz) |
| „halb X" Pseudo-Präzision | K28: „einen halben Tonwert" / K27: „einen halben Schritt" | `feedback_halb_praezision_tic` | ⚡ häufig | **ja** (regex) |
| Stakkato-Ketten — 3+ Sätze hintereinander < 6 Wörter | K27: „Hände flach. So bleiben. Nicht sprechen. Atmen." | `feedback_kein_stakkato_dialog` | ⚡ häufig | **ja** |
| Vollständige Sätze verletzt (Nominalsätze, Hänger) | K26: „Tee, dampfend" | `feedback_vollstaendige_saetze_default` | ⚡ häufig | teils (regex, falsch-positive hoch) |
| Default-Sein-Verb-Tic (lag/war/stand/saß) | K28 Sz3-Block: 6× `lag/lagen` in 430 W | `feedback_verb_praezision` | häufig | **ja** (Frequenz/Block) |
| Verquastete Sätze — Körperteil-Metaphern für Gedanken | „Der Gedanke saß unter dem Schlüsselbein" | `feedback_verquastung_katalog` | ⚡ sehr häufig | teils (Pattern-Katalog) |
| Kryptische Meta-Kommentare / Scharnier-Aphorismen | K23 (orig): „Zwei Menschen, die zusammen schweigen können, ist seit K21 neu" | `feedback_keine_kryptischen_meta_kommentare` | ⚡ häufig | teils (Pattern: „Das war der Preis", „So war es immer") |
| Gegen-Adverbien am Satzende als Ton-Flicken | „nennen, ernsthaft, wie die anderen" | `feedback_keine_gegen_adverbien_ton` | mittel | **ja** (Adverb-am-Satzende) |
| Anglizismen / Epoche-Bruch | „Debugging", „Charge", „Drift" als Bewertung | `feedback_keine_anglizismen_epoche` | mittel | **ja** (Wortliste) |
| „Puls/Pochen/Takt" als abstrakte Körper-Subjekte | „Pochen im Brustkorb" statt konkreter Stelle | `feedback_kein_puls` | ⚡ häufig | **ja** (grep + Kontext) |
| Foto-Vokabular auf Menschengesicht ohne Kamera | „Etwas in ihrem Gesicht verschob sich einen halben Tonwert" | `feedback_foto_vokabular_nicht_auf_gesicht` | mittel | **ja** (grep `Tonwert\|Grauwert` + Kontext) |
| Namen aus Negativliste (nordisch/friesisch/deutsch) | „Klaus", „Arne", „Henrik", „Thies" | `feedback_namen_negativliste` | mittel | **ja** (Negativliste) |
| Abstrakta-Stapel ohne Material-Verankerung | K23 (orig): „Zwei Menschen, die zusammen schweigen können" | `feedback_konkretheit`, `feedback_entwurf_klarer_stil` | häufig | teils (Abstrakta-Dichte) |

### Plot (Beat-Logik, Konkretion)

| Finding | Beispiel | Quelle | Häufigkeit | Auto-prüfbar? |
|---|---|---|---|---|
| Premature Doubt — Figur zweifelt vor ausgelöstem Ereignis | K30 (orig): Schwur-Ende „und dass er irgendwann dafür bezahlen wird" | `feedback_kein_puls` (Premature-Doubt) | häufig | teils (Kontext) |
| Eigenmächtige Canon-Additionen (neue Orte/Mechaniken) | K24: passive Moragh-Effekte als neue Welt-Regel | `feedback_keine_plot_additionen` | häufig | nein (Council/Canon-Wächter) |
| Gänsehaut-Moment fehlt oder zu schwach | Pre-Pipeline-Entwürfe ohne Pflichtfeld | Skill `entwurf.md` §Pflicht | mittel | **ja** (Header-Check + Mindest-Wortzahl) |
| Reihum-Dialog in Gruppenszenen | K19 Feedback: „nicht Schülergruppe, die nacheinander aufsagt" | `feedback_dialog_gruppenszenen` | mittel | nein (Council) |
| Entwurf-Sprache zu prosa-artig / Aphorismen im Exposé | K23 (orig): „das ist seit K21 neu" | `feedback_entwurf_klarer_stil` | häufig | teils (Aphorismus-Pattern) |
| Schwur/Versprechen ohne körperlichen Anker | K30 (orig): „dieses Wissen ist eine Tatsache, die in diesem Bett liegt" | diese Session | neu (B1-K30) | nein (Council-Frage) |
| BDSM Care-Beats fehlen nach Peak-Szene | K27 (orig): Vesper ohne Fürsorge-Beat | `feedback_bdsm_care_beats` | mittel | nein (VICTORIA-Council) |

### Welt (Setting, Demonik, Sinnes-Marker)

| Finding | Beispiel | Quelle | Häufigkeit | Auto-prüfbar? |
|---|---|---|---|---|
| Schemen demonisch unterspezifiziert (keine Hörner/Hufe/falsche Gelenke) | K30 (orig): nur „humanoid, schwarze Augen" | diese Session | neu (B1-K30) | nein (Welt-Bauweise) |
| Schemen als „Schemen" in Dialog/Prosa benannt | Figuren kennen Begriff nicht | `feedback_schemen_benennung` | mittel | teils (im Entwurf als Arbeitsbegriff ok; in Dialog-Info-Listen prüfen) |
| Salz/Metall auf Lippen außerhalb Maren-POV | bei Alphina/Sorel/Vesper nicht-canon | `feedback_kein_salz_metall_lippen` | selten | **ja** (POV+Pattern) |
| Sorel-Geruch nach Chemie in Nähe-Szenen | „Pyrogallol/Fixiersalz" in Intimszene | `feedback_sorel_geruch_nicht_chemie` | mittel | **ja** (grep + POV-Kontext) |

### Ton (Pathos, Heat, Genre-Match)

| Finding | Beispiel | Quelle | Häufigkeit | Auto-prüfbar? |
|---|---|---|---|---|
| Literary-knapp / telegrafisch statt commercial | K26: Substantiv-Phrasen ohne Verb, Inventar-Stil | `feedback_commerz_nicht_literarisch_knapp` | ⚡ häufig | teils (Stakkato + Ellipsen-Check) |
| Sorel mit Bart/Stoppel-Beschreibung | „Bartstoppeln auf seinem Kinn" | `project_sorel_kein_bart` | selten | **ja** (regex) |

---

## Empfehlungs-Cluster

### A — Top-8 für `scripts/entwurfs-check.py` (auto-prüfbar, häufig, low false-positive)

1. **Realweltliche Monatsnamen** — `Januar|Februar|März|April|Juni|...|Dezember` plus „Mai" gesondert (nur in Datums-Kontext, nicht als Eigenname).
2. **„Moragh" in Thalassien-POV-Dateien** — Heuristik: wenn Header POV/Setting nicht in Moragh, dann grep `\bMoragh\b`.
3. **„nicht X, sondern Y"** — regex `\bnicht\b[^,.;]{1,40},?\s+sondern\b`.
4. **„halb X" Pseudo-Präzision** — regex `\bhalb(?:en?|er?|e?)\s+\w+`.
5. **Anglizismen / Epoche-Bruch** — Wortliste: `Debugging|Debug|Charge|Drift|Setup|Feedback|Input|Output|Update|gecheckt|gefixt|Workflow|Briefing`.
6. **Kleidungs-Anachronismen** — `\b(Jacke|Bluse|Jacken|Blusen|Jackentasche)\b`.
7. **Metrische Maßeinheiten** — `\b\d+\s*(Meter|Kilometer|Zentimeter|Millimeter|Kilogramm|cm|km|kg|mm)\b`.
8. **Stakkato-Ketten** — 3+ aufeinanderfolgende Sätze mit < 6 Wörtern in Prosa-Zeilen.

Bonus: **Sein-Verb-Häufung** (lag/war/stand/saß > 2× pro 150-Wort-Block) als Hinweis ohne harte Schwelle.

### B — Top-5 für Canon-Wächter-Subagent (Memory-Abgleich, semantisch)

1. **Sorel-Prinzip / Figurenwissen** — Pro Figur: Was weiß sie laut letzten 3 Kapitel? Weiß sie hier mehr? Bei Eigennamen, Mechaniken, Cross-Kapitel-Wissen.
2. **Schemen-Magie-Modus + Lautlosigkeit** — Bei Schemen-Kontakt: ist Magie-Modus (Eis/Feuer/etc.) explizit gesetzt? Lautlosigkeit als Marker erwähnt? Berührung ohne Magie → kein Schaden? (Memory `project_schemen_magie_modi.md`)
3. **Spukgeschichte ab K21** — Passiv-Effekte (Kerzen, Objekte, Raumreaktionen) ohne benannte Urheberin in Kapiteln ≥ K21? Memory `feedback_keine_spukgeschichte.md`.
4. **Plot-Additionen** — Neue Orte, Mechaniken, Symbole gegen `00-canon-kompakt.md` + `00-welt.md` abgleichen. Memory `feedback_keine_plot_additionen.md`.
5. **Figuren-Aufstellungen** — „die Vier" vs. „die Fünf" (Runa schleicht erst beim Portal mit), Du/Sie-Stand pro Paar/Kapitel, BDSM-Register nur Vesper/Maren.

### C — Manuell bleiben (Council/Autor)

1. **Reihum-Dialog in Gruppenszenen** — narrativer Rhythmus ist nicht regex-fähig; Beziehungs-Lektorin-Subagent.
2. **Gänsehaut-Moment trägt emotional?** — Pflichtfeld kann auf Vorhandensein geprüft werden, aber ob er trägt, ist Council-Urteil (LINA/KAYA).
3. **Schwur/Versprechen mit körperlichem Anker?** — Strukturanalyst-Frage: hängt der Schwur an einer Stelle/einem Ding, oder ist er Abstraktum?
4. **BDSM Care-Beats** — VICTORIA-Council, Kontext-Lesen nötig.
5. **Demonik-Inventar Schemen** — Welt-Bauweise; Autor entscheidet Setting-Detail.

---

## Verwendung

- **`scripts/entwurfs-check.py {ID}`** in `/entwurf` Phase 4.1 vor dem Logik-Subagent. Output ist eine Markdown-Tabelle mit Findings; geht in den konsolidierten Bericht (Phase 6).
- **Canon-Wächter-Subagent** in `/entwurf` Phase 5 als drittes Subagent neben Strukturanalyst und Beziehungs-Lektorin. Liest Memory-Files + Entwurf, prüft Top-5 semantische Konsistenz.
- **Council-Leserinnen** in Phase 5b decken die manuell-bleibenden Findings ab (Beat-Stärke, Pacing, Genre-Match).

**Pflege:** Wenn neue wiederkehrende Findings auftreten (z.B. nach mehreren Entwürfen ein neues Memory entsteht), diese Datei + das Skript ergänzen. Drift verhindern: ein Memory = ein Eintrag hier.
