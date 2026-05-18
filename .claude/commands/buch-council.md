# /buch-council — Buch-Level-Commercial-Council (5 Leserinnen-Archetypen lesen den ganzen Bogen)

Reviewt **Buch 1 als Ganzes** (oder eine Akt-Auswahl) gegen das 95%-Commercial-Gate aus `buch/00-positioning.md` Abschnitt 9. Fünf Leserinnen-Archetypen (LINA / NORA / MEIKE / VICTORIA / KAYA) lesen den Bogen mit Buch-Sicht und urteilen: **Wo hätte ich aufgehört? Was wurde mir versprochen und nicht geliefert? Würde ich Buch 2 kaufen?**

**Abgrenzung zu `/szene-council`:**
- `/szene-council` = Scene-/Leseprobe-Level (200-Wörter-Hook, vier Pflichten, Mikro-Findings pro Stimme)
- `/buch-council` = Buch-/Akt-Level (Bogen-Verdict, Drop-Off-Kapitel, Genre-Promise über alle Kapitel, Buy-Decision für Folgeband)

Nicht Handwerks-Mikrofindings — dafür `/refit`, `/stil-check`, `/lektorat-fix`.

## Input

Argumente (alle optional):
- **Scope:** `b1` (Default — ganzes Buch 1) | `akt1` | `akt2` | `akt3` | `akt4` | Kapitel-Range `K12-K22`
- **Modus:** `key` (Default — Schluesselszenen + Akt-Uebergaenge, ~30k Woerter pro Persona) | `full` (alle finalen Kapitel des Scopes, ~170k Woerter Buch 1)
- **Personas:** Liste mit Komma `lina,nora,meike,victoria,kaya` (Default = alle 5)

Beispiele:
- `/buch-council` → Buch 1 komplett, key-Modus, 5 Personas
- `/buch-council full` → Buch 1 komplett, alle Kapitel, 5 Personas
- `/buch-council akt3 full lina,victoria` → Akt III komplett, nur LINA + VICTORIA

Wenn `full` und Scope = `b1`: bestaetige beim Autor (teuer: ~5 × 250k Tokens lesend).

## Pflicht-Lade-Reihenfolge (Hauptsession, vor Subagent-Spawn)

1. **`buch/00-positioning.md` ganz** — fuer das 95%-Gate und die Genre-Vektoren.
2. **`buch/status.json`** ueber `scripts/kapitel-kontext.py` ODER direkt — fuer die kanonische Kapitel-Reihenfolge des Scopes (`akte[*].kapitel`).
3. **`buch/synopse-b1.md`** falls vorhanden — fuer Bogen-Promise-Check.
4. **`buch/_findings-format.md`** — Block-Format gilt fuer die persona-spezifischen Top-3-Stellen-Verweise (Stelle + warum, keine Tagging-Pflicht, weil das hier Bogen-Urteil ist und nicht Mikrofindings).

**Nicht laden in Hauptsession:** die Kapitel-Prosa selbst. Das tun die Subagenten.

## Schluesselszenen-Definition (fuer `key`-Modus)

Pro Akt liest jeder Persona-Subagent:
- **Akt-Eroeffnungskapitel** (erstes Kapitel des Akts)
- **Akt-Schlusskapitel** (letztes Kapitel des Akts)
- **Akt-spezifische Pflicht-Szenen:**
  - **Akt I:** K01 (Hook), K09/K10/K11 (erste Resonanz-Beruehrungen), K12 (Alphina+Sorel-Schwelle)
  - **Akt II:** K15 (Steinkreis-Eskalation), K17 (Maren/Vesper-Schwelle), K21 (erster Sex Alphina/Sorel — Heat-Probe)
  - **Akt III:** K26 (Vesper-Wendepunkt), K27_5 (Vesper-BDSM), K29/K30 (Sorel-Magie-Tot­zone), K33 (Akt-Cliff)
  - **Akt IV:** K35 (Maren-Tor-Entscheidung), K38/K39 (Alphina-Trauer/Aufbruch), K40 (Epilog/Cliff B2)
- **Interludes** I1, I2, I3 — alle drei (kurz, hoher Informationswert)
- **Plus 2 vom Persona gewuenschte Stichproben-Kapitel** (Subagent darf selbst whlen, was er noch lesen will, sobald er die Pflicht-Liste durch hat)

Das `key`-Set ist persona-uebergreifend gleich (~18 Kapitel), damit die Verdicts vergleichbar sind. Persona-Stichproben sind on top.

## Die fuenf Stimmen

Erbe aus `/szene-council`: **LINA** (Romantasy, 28) · **NORA** (Dark Romance, 34) · **MEIKE** (Dark Fantasy, 31) · **VICTORIA** (BDSM, 38) · **KAYA** (Dystopie/Grimdark, 26). Voll-Briefs siehe `.claude/commands/szene-council.md` Abschnitt „Die fuenf Stimmen" — nicht hier wiederholen.

**Buch-Level-Spezifikum pro Stimme** (zusaetzlich zum Scene-Brief):

| Stimme   | Bogen-Frage |
|----------|-------------|
| LINA     | Wurde mir Alphina/Sorel als Romance-Bogen sauber serviert — Slow-Burn → First Touch → First Time → Riss/Tod → emotionale Reparatur fuer B2? Hatte ich genug Swoon-Momente? Trug das Ende emotional, obwohl Sorel stirbt? |
| NORA     | Bleibt Power-Dynamik (Alphina-Top, Vesper-Dom) konsequent? Kaempfen die Frauen oder werden sie geschoben? Bleibt die Schaerfe ueber alle Akte oder verflacht sie in der Mitte? |
| MEIKE    | Welt mit Zaehnen ueber 168k Woerter oder verliert Vael den Biss? POV-Disziplin ueber 5 Figuren konsequent? Gruppen-Dynamik im Tor-Finale glaubwuerdig? |
| VICTORIA | Vesper/Maren-BDSM-Linie: Material-Konsistenz, Aftercare, Psychologie ueber den ganzen Bogen? Alphina/Sorel als Top/Bottom-Variante glaubwuerdig (selten im Markt)? Heat-Korridor sauber (kein Vulgaer-Slip, kein Kitsch-Slip)? |
| KAYA     | Sorel-Tod ohne literary-Ausweichen? Gewalt mit Folge? Wo hat das Buch sich vor Haerte geduckt? Genuegt Buch 1 fuer eine Dystopie-erfahrene Leserin oder ist es ihr „nur Romance"? |

## Ablauf

**Phase 0 — Setup.** Hauptsession liest Pflicht-Dateien, baut Kapitel-Pfad-Liste fuer Scope + Modus, bestaetigt bei `full b1` beim Autor.

**Phase 1 — Persona-Subagenten parallel.** Pro aktiver Persona ein Subagent (`general-purpose`, default-Modell), gespawnt im selben Message-Block. Subagent-Prompt-Template siehe unten. Subagenten arbeiten unabhaengig, kennen sich nicht.

**Phase 2 — Subagent-Output sammeln.** Jeder Subagent liefert das untenstehende Persona-Output-Format.

**Phase 3 — Synthese-Tabelle.** Hauptsession baut die Master-Tabelle (5 Stimmen × Bogen-Metriken). Spalten: Score, Drop-Off-Kapitel, Top-Staerke, Top-Schwaeche, Buy-Decision B2.

**Phase 4 — Konvergenz-Befunde.** Hauptsession extrahiert die Stellen, an denen ≥3 Stimmen unabhaengig dieselbe Lücke / dasselbe Lob nennen. Das sind die echten Buch-Signale (Einzelpersona = subjektiv, Konvergenz = Markt-Signal).

**Phase 5 — Top-5-Buch-Fixes priorisiert.** Aufwand × Wirkung. Jeder Fix nennt:
- Was (Kapitel + 1-Satz-Diagnose)
- Welche Stimmen forderten es (Initialen)
- Aufwand-Schaetzung (Mikro/Mittel/Gross) — Mikro = Sweep, Mittel = Szene um/neu, Gross = mehrere Kapitel
- Erwartete Score-Bewegung

**Phase 6 — Buy-Decision-Aggregat.** Wieviele der zustaendigen Stimmen wuerden Buch 2 kaufen? `5/5` = bestanden, `4/5` = grenzwertig, `≤3/5` = Bogen-Problem.

## Subagent-Prompt-Template (Persona X)

> Du bist **{PERSONA-NAME}**, {Alter}, Leserin aus dem {Genre}-Regal. Voll-Brief: `.claude/commands/szene-council.md` Abschnitt „Die fuenf Stimmen" — Persona „{PERSONA-NAME}". Lies das einmal.
>
> Du liest jetzt **{Scope}** von „Der Riss" als Buch, nicht als Mikrofindings-Lauf. Du bist Endkundin, keine Kritikerin.
>
> **Lade in Reihenfolge:**
> 1. `buch/00-positioning.md` (Genre-Promise, dein Genre-Vektor)
> 2. Diese Kapitel in genau dieser Reihenfolge: `{Liste der Pfade}`
> 3. Optional 2 Stichproben deiner Wahl aus `buch/kapitel/` (final-Dateien, keine entwurf/handoff)
>
> **Beantworte (in deiner Stimme, in-character):**
>
> **1. Drop-Off-Test.** Wo waerst du ausgestiegen, wenn das nicht deine Lese-Hausaufgabe waere? Nenne Kapitel + 1-Satz-Grund. Wenn du nirgends ausgestiegen waerst, sag es.
>
> **2. Genre-Promise.** Welche Versprechen aus Akt I hat das Buch dir bis Akt IV eingeloest? Welche nicht? Konkrete Liste, je 1 Satz.
>
> **3. Pacing-Bogen.** Wo war dir zu schnell, wo zu langsam? Nenne Akt + Kapitel-Range, kein Mikro.
>
> **4. Figuren-Bogen.** Welche der 5 POV-Figuren (Alphina, Sorel, Vesper, Maren, Runa) hat dich getragen? Welche hast du verloren? Warum?
>
> **5. Top-3-Staerken** (Bogen-Level, nicht Satz-Mikro). Format: `Kapitel-ID — was du behalten wuerdest — warum es trug`. Mit kurzer Zitat-Stelle (1-2 Saetze max).
>
> **6. Top-3-Schwaechen** (Bogen-Level). Format: `Kapitel-ID — was nicht trug — was du brauchst statt dessen`.
>
> **7. Persona-Bogen-Frage** (dein Spezial-Thema laut buch-council-Skill — der Skill-Aufruf nennt sie dir): Beantworte sie ehrlich.
>
> **8. Commercial-Score 0-100.** Skala: 90+ = ich kaufe und empfehle, 80-89 = ich kaufe, 70-79 = ich lese kostenlos, <70 = ich lege weg.
>
> **9. Buy-Decision B2.** Kaufst du Buch 2? `Ja` / `Vielleicht` / `Nein` + 1 Satz Grund.
>
> **Regeln:**
> - In-character, nicht neutral-akademisch.
> - Wenn ein Akt nicht dein Register ist (z.B. KAYA bei reinem Romantasy-Akt), sag „kein Verdict, nicht mein Register" mit Begruendung — nicht silently bewerten.
> - Keine Canon/Logik-Korrekturen (das macht `/logik-check`/`/figuren-check`).
> - Keine Stil-Mikrofindings (das macht `/stil-check`).
> - Wenn du eine konkrete Szene zitierst: 1-2 Saetze max, mit Kapitel-ID.
>
> **Output-Format strikt:**
>
> ```
> ## {PERSONA-NAME} — Buch-Verdict
>
> **Drop-Off:** {Kapitel oder „nirgends"} — {Grund}
>
> **Genre-Promise:**
> - eingeloest: {Liste}
> - nicht eingeloest: {Liste}
>
> **Pacing-Bogen:** {Akt-/Kapitel-Range mit zu-schnell / zu-langsam}
>
> **Figuren-Bogen:**
> - traegt: {Liste mit 1-Satz-Grund}
> - verloren: {Liste mit 1-Satz-Grund}
>
> **Top-3-Staerken:**
> 1. K{XX} — {was} — {warum}
>    > „{Zitat 1-2 Saetze}"
> 2. ...
> 3. ...
>
> **Top-3-Schwaechen:**
> 1. K{XX} — {was nicht trug} — {was du brauchst}
> 2. ...
> 3. ...
>
> **Persona-Bogen-Frage:** {Antwort}
>
> **Score:** {0-100}
>
> **Buy B2:** Ja / Vielleicht / Nein — {1 Satz}
> ```

## Hauptsession-Output-Format

````markdown
# /buch-council — {Scope} · {Modus} · {Datum}

**Gelesen:** {Kapitel-Liste oder Range}
**Wortzahl im Scope:** {N}
**Personas aktiv:** {Liste}

---

## Phase 2 — Persona-Verdicts

{Pro Persona der vollstaendige Subagent-Output, unveraendert eingebettet}

---

## Phase 3 — Synthese-Master-Tabelle

| Stimme    | Score | Drop-Off  | Top-Staerke           | Top-Schwaeche        | Buy B2 |
|-----------|-------|-----------|-----------------------|----------------------|--------|
| LINA      | XX%   | K{XX} / — | K{XX}: {Stichwort}    | K{XX}: {Stichwort}   | Ja/V/N |
| NORA      | ...   | ...       | ...                   | ...                  | ...    |
| MEIKE     | ...   | ...       | ...                   | ...                  | ...    |
| VICTORIA  | ...   | ...       | ...                   | ...                  | ...    |
| KAYA      | ...   | ...       | ...                   | ...                  | ...    |
| **Durchschnitt (zustaendige)** | XX% |   |                  |                      | X/5    |

**Niedrigste zustaendige Stimme:** {Name} mit {Score}% — das ist das Risiko-Signal.

---

## Phase 4 — Konvergenz-Befunde (≥3 Stimmen einig)

**Konvergente Staerken:**
- {Was} — Stimmen: {LINA, NORA, MEIKE}
- ...

**Konvergente Luecken:**
- {Was} — Stimmen: {NORA, VICTORIA, KAYA}
- ...

Stand-alone-Stimmen (nur 1-2 Personas) gehen nach Phase 5 als „nachrangig" durch oder werden verworfen.

---

## Phase 5 — Top-5-Buch-Fixes (priorisiert)

1. **[{Aufwand}]** K{XX}-K{YY}: {Diagnose 1 Satz} — gefordert von {Stimmen} — erwartete Wirkung: +{N}% Durchschnitt
2. ...
3. ...
4. ...
5. ...

Reihenfolge: Aufwand-Wirkung-Quotient (Mikro mit hoher Wirkung zuerst).

---

## Phase 6 — Verdict

- **Commercial-Durchschnitt:** XX%
- **Buy-Decision-Aggregat:** X/5
- **Status:** BESTANDEN (≥90% UND ≥4/5 Buy) | GRENZWERTIG (≥75% UND ≥3/5 Buy) | NACHARBEIT (sonst)

**Empfehlung:** {1-3 Saetze, was als naechstes ansteht}
````

## Gate-Protokoll

Nach Phase 6:
1. Zusammenfassung in max 5 Zeilen.
2. Frage: **„Top-5-Fixes umsetzen, eine Persona vertiefen (Folge-Dialog), oder erst andere Sicht (Trocken-Pass `/figuren-check` + `/logik-check` + `/stil-check`) ueber den Bogen?"**

**Keine automatischen Fixes.** Buch-Level-Council ist Diagnose, nicht Therapie. Therapie macht der Autor mit gezielten Skill-Laeufen pro Fix.

## Token-Hinweis

- `key`-Modus, 5 Personas, ~18 Kapitel × ~4k Woerter = ~360k Woerter Read-Volumen ueber alle Subs (parallel, jeder ~72k pro Sub). Handhabbar.
- `full`-Modus, 5 Personas, 44 Kapitel × ~3.8k = ~835k Woerter (~1.25M Tokens) Read-Volumen. **Teuer.** Nur fuer Endgegner-Pass vor Lektoratsabgabe.

Wenn `full b1` aufgerufen wird: explizit nachfragen `„Full-Pass kostet ca. 5 × 250k Tokens lesend. Bestaetigen?"`.

$ARGUMENTS
