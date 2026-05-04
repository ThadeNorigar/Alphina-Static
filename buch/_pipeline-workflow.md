# Pipeline-Workflow — Der Riss

**Stand 2026-05-04 — nach Voice-Anchoring + Antislop + Vision-Layer + Tschechow-Ledger + Plateau-Detection.**

Best-Practice-Pattern aus NousResearch/autonovel + Agents' Room (DeepMind) + eigene K31-Erfahrung. Quelle: `_autor-feedback-katalog.md` + Recherche-Sitzung 2026-05-04.

## Architektur-Überblick

Drei Schichten:

| Schicht | Was | Wo |
|---|---|---|
| **1. Welt-Bible** | Welt, Stilregeln, Stimme, POV-Dossiers, Schreibblätter, **Voice-Exemplars (NEU)**, Tschechow-Ledger (NEU) | `buch/00-welt.md`, `buch/02-stilregeln-v2.md`, `buch/01-autorin-stimme.md`, `buch/pov/<figur>.md`, `buch/pov/<figur>-schreibblatt.md`, **`buch/pov/<figur>-voice-exemplars.md`**, **`buch/_tschechow-ledger.md`** |
| **2. Aktpläne + Storyline** | Beats pro Akt, Gesamtbogen, Zeitleiste | `buch/04-akt3.md`, `buch/05-akt4.md`, `buch/00-storyline.md`, `buch/zeitleiste.json` |
| **3. Pipeline-Skills** | `/entwurf` → `/ausarbeitung` → `/refit` (alt) / `/leseprobe-refit` | `.claude/commands/*.md` |

Plus mechanische Filter: `scripts/antislop-check.py` (Layer-1-Pattern-Filter, Exit 0/1/2).

---

## A. Buch definieren (einmalig pro Buch)

**Pflicht-Dateien VOR dem ersten Kapitel-Entwurf:**

1. **Welt-Bible**
   - `buch/00-welt.md` — Orte, Fraktionen, Technologie, Pflanzen, Monate
   - `buch/zeitleiste.json` — Single Source of Truth für Reihenfolge
   - `buch/00-positioning.md` — Marktposition, Zielgruppe, Stilvektoren, 95%-Gate (Pflicht-Lese vor jeder Prosa-Session)

2. **Stil + Stimme**
   - `buch/01-autorin-stimme.md` — Drei Register, Begehren-Vokabular, Anti-Patterns
   - `buch/02-stilregeln-v2.md` — Harte Limits + Default-Deny
   - `buch/01-referenz-konkretheit.md` — Material-Erstnennung, Vorfeld-Inversion, Sinnes-Trias

3. **Magie + Kanon**
   - `buch/10-magie-system.md` — Mechanik
   - `buch/00-storyline.md` — Gesamtbogen
   - `buch/_tschechow-ledger.md` — **NEU:** zentrales Plant→Payoff-Tracking

4. **Pro POV-Figur** (Pflicht!)
   - `buch/pov/<figur>.md` — Dossier (Wound/Want/Need/Lie, Wissen, Berufslinse)
   - `buch/pov/<figur>-schreibblatt.md` — Schreib-Bausteine (Magie BILD/QUELLE/FOLGE, Heat-Stellen, Lieblingswörter, Anti-Patterns, Hooks, Sie/Du-Status)
   - **`buch/pov/<figur>-voice-exemplars.md`** — **NEU PFLICHT:** 3–5 kuratierte Passagen aus etablierten Final-Kapiteln, die die gewachsene Stimme verkörpern

5. **Aktpläne** (pro Akt)
   - `buch/0X-aktN.md` — Beats, Tschechow-Ankündigungen, Kapitel-Liste

**Bei NEUER POV-Figur:**
- Wenn noch keine Final-Kapitel existieren → `/voice-discovery <figur>` aufrufen (5 Trial-Passages, Autor wählt, Exemplars werden kuratiert).
- Wenn etablierte Stimme aus 5+ Final-Kapiteln vorhanden → manuell aus den besten Passagen kuratieren.

---

## B. Kapitel entwerfen — `/entwurf <ID>`

**Phase 0** — Guard-Checks (Modell, Status)
**Phase 1** — Kontext laden (POV-Dossier, Aktplan, Tschechow-Ledger)
**Phase 2** — Plot-Beats sachlich schreiben (kein Prosa-Mimikry, klar und belastbar)
**Phase 3** — Status setzen + Deploy
**Phase 4** — Auto-Pattern-Check + Logik-Check
**Phase 5** — Entwurfs-Council (Strukturanalyst, Beziehungs-Lektorin, Canon-Wächter — parallel, sonnet)
**Phase 5b** — Council-Leserinnen-Review (LINA/NORA/MEIKE/VICTORIA/KAYA — 2-3 Stimmen je nach Heat/Plot-Charakter)
**Phase 6** — Konsolidierter Bericht
**Phase 7** — Feedback-Loop (Autor entscheidet)
**Phase 8** — bei *„entwurf ok"*:
- 8.1 Status `entwurf-ok`
- **8.1b — NEU: Tschechow-Ledger updaten** — alle Plants des Entwurfs in `_tschechow-ledger.md` eintragen (Status `geplant`, neue IDs vergeben)
- 8.2 Handoff-File für `/ausarbeitung` generieren (mit Voice-Exemplars-Verweis pro Szene)
- 8.3 Harter Stop — neue Session

---

## C. Kapitel ausarbeiten — `/ausarbeitung <ID>`

**Phase 0** — Guard-Checks (Status `entwurf-ok`? Handoff vorhanden? Modell Opus?)
**Phase 1** — Kontext laden (~17–22k W):
- Positioning, Entwurf, Handoff, POV-Dossier, **POV-Schreibblatt (4a)**, **Voice-Exemplars (4b NEU)**, Stilregeln, Konkretheits-Referenz, Autorin-Stimme, Ton-Referenz-Kapitel, Council-Leserinnen-Profile

**Phase 1.5** — Pre-Check-Setup-Pflichten:
- Schritt A: Memory + Anti-Patterns verinnerlichen
- Schritt B: Bühnen-Inventar-Skizze (Lichtquellen, Personen, Objekte, Magie-Status)
- Schritt C: Magie-Beat-Templates ausfüllen (BILD/QUELLE/FOLGE pro Magie-Akt)
- Schritt D: Hook-Test (Z.1 gegen Anti-Hook-Muster)
- Schritt E: Pre-Check-Liste an Autor + Council-Damen festlegen

**Phase 2** — Block-für-Block schreiben (3–5 Absätze, ~150–500 W pro Block):

```
LOOP PRO BLOCK:

Stage 0: Schreib-Subagent (sonnet) mit Voice-Anchoring
  ├─ 2 Voice-Exemplars wörtlich im Prompt
  ├─ Pre-Check-Liste + Pre-Writing
  └─ Output: 150–500 W, NICHT ins File

Stage 1: Antislop-Layer-1
  ├─ python scripts/antislop-check.py _tmp_block.md
  ├─ Exit 2 (PFLICHT) → REJECT-REGENERATE (zurück Stage 0, Iter++)
  ├─ Exit 1 (TIC) → Findings für Stage 4 sammeln
  └─ Exit 0 → weiter

Stage 2: 5 Subagenten parallel (sonnet)
  ├─ Sprach-TÜV (Pattern-Verstöße)
  ├─ Verquastungs-Detektor (Mündlicher Lese-Test)
  ├─ Konsistenz-Wächter (Bühne, Magie, POV, Welt)
  ├─ Genre-Leserin (LINA/NORA/MEIKE/VICTORIA/KAYA)
  └─ Vision-Layer (NEU: Stimme-Treffer + Sog + Emotion + Plot-Twist-Setup)

Stage 3: Konsolidieren
  ├─ PFLICHT (harte Verstöße) → REJECT-REGENERATE
  ├─ EMPFEHLUNG (TIC, Vision-Lücken) → Stage 4
  └─ STIL-VORBEHALT → Autor entscheidet

Stage 4: Inline-Fixes (nur EMPFEHLUNG)
Stage 5: Re-Check (Verquastungs-Detektor auf gefixten Block)
Stage 6: Block ins File
Stage 7: Bericht an Autor (Voice-Score, Findings, starke Beats, Vision-Lücken, Verdikt)

WARTE auf Autor-OK → nächster Block
```

**Plateau-Detection (HART):**
- Iter ≥ 3 oder Findings-Diff = 0 → STOPP
- Eskalation: (a) Opus-Schreib-Subagent (b) manueller Rewrite (c) Plot-Beat zurück zum Entwurf

**Phase 3** — Status `ausarbeitung` + Deploy
**Phase 4** — Stil-Check (Subagent, sonnet)
**Phase 5** — Final Council (3 Subagenten sequenziell)
**Phase 5.5** — Autorin-Durchgang (Subagent, opus)
**Phase 6** — Konsolidierter Bericht
**Phase 7** — Fixes-Loop
**Phase 8** — Status `final` + Deploy + kapitel-summaries.md + Tschechow-Ledger updaten (`geplant` → `geladen`/`abgefeuert`) + Handoff löschen + Commit
**Phase 9** — Harter Stop

---

## D. Leseprobe definieren + refitten — `/leseprobe-refit`

**Definieren** (für Marketing/Stil-Test, oft vor Kapitel-Final):
- Mini-`/ausarbeitung`-Pass auf 1 Szene aus geplantem Kapitel
- Block-Loop läuft, Voice-Exemplars-Anchor sichert POV-Konsistenz auch separat

**Refit** (4-Schritt-Pipeline):
1. **Antislop-Layer-1-Pass** auf Probe → Findings-Cluster
2. **Neuschrieb-Subagent** mit `voice-exemplars.md` + Antislop-Findings als Brief
3. **5 Subagenten parallel** (inkl. Vision-Layer) prüfen Neuschrieb gegen Voice-Exemplars
4. **Autor-Abnahme**

**Plateau:** max 3 Refit-Pässe, dann Autor entscheidet (akzeptieren / manuell rewriten / verwerfen).

---

## E. Alte Kapitel refitten — `/refit <ID>`

**Phase 0** — Stil-Gap-Check entscheidet Modus:
- ≥ 5 Treffer (Antithese, halb-X, sie dachte etc.) → **Modus A** (Plot-Lock-Refit + Neuausarbeitung via `/ausarbeitung`)
- < 5 Treffer → **Modus B** (Pipeline-Check auf bestehendem Text)

**Modus A:**
- Plot-Lock aus Altkapitel extrahieren → regulärer `/entwurf` → `/ausarbeitung`
- Bekommt automatisch alle neuen Settings (Voice-Anchoring, Vision-Layer, Antislop, Plateau)
- Altkapitel wird archiviert

**Modus B (Pipeline-Check):**
1. **Phase B0** — Antislop-Layer-1-Pass auf ganzes Kapitel
2. **Phase B1** — Kontext laden inkl. **`voice-exemplars.md`** und **`_tschechow-ledger.md`**
3. **Phase B2** — 5 Subagenten parallel (Sprach-TÜV, Verquastung, Konsistenz, Genre-Leserin, **Vision-Layer NEU**) auf Kapitel-Scope
4. **Phase B3** — Konsolidierung (3-Block-Master-Tabelle: PFLICHT / EMPFEHLUNG / STIL-VORBEHALT)
5. **Phase B4** — Fix-Loop mit Plateau-Detection (max 3 Pässe, Score-Δ < 5% → Stopp)
6. **Phase B5** — Status-Update + Deploy

**Anwendung:** K1–K22 (alt-Stil, vor Pipeline) lassen sich kapitelweise auf K23–K30-Niveau heben. Voice-Exemplars sind dabei der Anker — Subagenten messen Stimme-Treffer direkt.

---

## F. Pflicht-Files-Matrix pro Skill

| Skill | Voice-Exemplars | Tschechow-Ledger | Antislop | Vision-Layer | Plateau |
|---|---|---|---|---|---|
| `/entwurf` | – | ✅ Update (8.1b) | – | – | – |
| `/ausarbeitung` | ✅ Pflicht-Lade (4b) + im Schreib-Prompt zitiert | ✅ Lese + Update bei final | ✅ Layer-1 vor Subagenten | ✅ Subagent 5 | ✅ Iter ≥ 3 |
| `/refit` Modus A | ✅ via /ausarbeitung | ✅ via /ausarbeitung | ✅ Phase B0 | ✅ via /ausarbeitung | ✅ via /ausarbeitung |
| `/refit` Modus B | ✅ Phase B1 | ✅ Phase B1 | ✅ Phase B0 | ✅ Phase B2 Subagent 5 | ✅ Phase B4 |
| `/leseprobe-refit` | ✅ im Neuschrieb-Brief | – | ✅ Schritt 1 | ✅ in Schritt 3 | ✅ max 3 Pässe |
| `/logik-check` | – | ✅ Phase 4b Validierung | – | – | – |

---

## G. Voice-Discovery (optional, neu) — `/voice-discovery <figur>`

**Wann:**
- Neue POV-Figur ohne Final-Kapitel
- Etablierte Stimme nach 10+ Kapiteln driftet (Refresh)

**Workflow:**
1. Subagent schreibt 5 Trial-Passages (200–300 W) für dieselbe Szene in unterschiedlichen Registern
2. Autor wählt 1–2 beste aus
3. Exemplars werden extrahiert + Stil-Marker formuliert
4. `pov/<figur>-voice-exemplars.md` wird erstellt

**NICHT für etablierte POVs** (Alphina/Sorel/Vesper/Maren) — die haben K1–K30 als Anker.

---

## H. Adversarial-Edit (später) — `/cuts <kapitel>`

Pattern aus NousResearch/autonovel: Cuts-Pass nach Final-Status, klassifiziert nur (kein Rewrite):
- OVER-EXPLAIN (~32% bei autonovel-Korpus)
- REDUNDANT (~26%)
- UNCLEAR

Output: Cuts-Vorschläge zur Autor-Abnahme. Wann nutzen: vor Final-Submission, oder bei Kapiteln über Wortziel.

---

## Pipeline-Investitionsbilanz

**Token-Budget pro Block (Phase 2):** ~40k (Schreib-Subagent ~5k + 5 Check-Subagenten ~5–8k je + Konsolidierung + Fixes + Re-Check). Bei ~9 Blöcken/Kapitel: ~360k Tokens.

**Token-Budget pro Refit Modus B:** ~80–120k (Antislop + 5 Subagenten + 1–3 Fix-Loops).

**Was sich gegenüber Vor-2026-05-04 ändert:**
- Stage 0 Schreib-Subagent ersetzt Hauptsessions-Schreiben → mehr Token, aber stabilere Stimme
- Layer-1 Antislop fängt Pattern-Verstöße automatisch → Subagenten 1–4 fokussieren Layer 2
- Vision-Layer (Subagent 5) verankert positive Marker → kein „bestanden" ohne Stimme-Treffer
- Reject-Regenerate statt Inline-Fix → kein Whack-a-Mole
- Plateau-Detection → harter Stopp, statt 6+ Iterationen wie bei K31-Sz1

**Quellen der Architektur:**
- [NousResearch/autonovel PIPELINE.md](https://github.com/NousResearch/autonovel/blob/master/PIPELINE.md) — Voice-Fingerprint, Reject-Regenerate, Plateau-Detection, Reader-Panel
- [NousResearch/autonovel CRAFT.md](https://github.com/NousResearch/autonovel/blob/master/CRAFT.md) — Six positive Marker (Spezifität, Subtext, Restraint, Stille, Rhythmus-Variations-Koeffizient, Earned Metaphor)
- [Agents' Room (DeepMind, OpenReview)](https://openreview.net/forum?id=HfWcFs7XLR) — Orchestrator-Worker, Scratchpad, Section-by-Section
- Eigene Erfahrung: K31-Sz1 v1–v6 (was nicht funktioniert: Inline-Fix-Iterationen)
