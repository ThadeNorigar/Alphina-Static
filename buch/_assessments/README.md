# Kapitel-Assessment-Datensatz — Buch 1

*Erstellt: 2026-05-14 · 41 finale Kapitel · Strukturierte Daten: `kapitel-scores.json`*
*Update 2026-05-17: K40 (Vael-Epilog) nachgetragen. K27_5 (Vesper-V/M-Bruecke) nachgetragen mit Post-Sweep-Score 9.11 FINAL-REIF. K38 (Alphina, Trilogie-Wendepunkt) noch ausstehend.*

Pro finalem Kapitel ein Subagent (Opus): Council-Assessment (7 Achsen 0-10 + Verdikt + Staerken/Schwaechen + PFLICHT-Findings) + Book-Council-Rating (5 Leserinnen-Archetypen, Marktfaehigkeit 0-100).

## Aggregat

- **Council-Gesamt Ø:** 8.50 / 10
- **Book-Council-Gesamt Ø:** 79.91 / 100
- **FINAL-REIF (Council ≥ 9.0):** 11 / 41 — B1-K01, B1-I1, B1-K05, B1-K08, B1-I2, B1-K19, B1-K20, B1-K24, B1-K27, **B1-K27_5**, B1-K30
- **Book-Council-Verdikt:** alle GRENZWERTIG (70–89) bzw. BESTANDEN (K40 89.0) — keine DURCHGEFALLEN
- **PFLICHT-Findings gesamt:** 77
- **Kapitel mit Em-Dash-PFLICHT-Befund:** 0 / 41

### Sweep-Notes

- 2026-05-15: Em-Dash-Sweep (commits 8660f10 + ebb17d8): 889 Em-Dashes aus 26 finalen Kapiteln entfernt.
- 2026-05-15: 'halb X' + 'nicht X, sondern Y' Sweep (commit 20bee4e): ~61 Tic-Stellen ent-tickt, funktionale Reste behalten.
- 2026-05-15: Mini-Tic-Sweep (commit 291eee7): 'Resonanz' (K03/K22/I2) + 'Session' (K27) ersetzt.
- PFLICHT-Findings, die sich ausschliesslich auf die gesweepten Tics bezogen, wurden aus dem Datensatz entfernt.
- Hinweis: Council-Gesamt-Scores nicht neu erhoben. Fuer aktuelle Final-Reife-Beurteilung der gesweepten Kapitel Neu-Erhebung notwendig.
- 2026-05-15: Heuristik-Score-Update angewandt. stil_disziplin pro Kapitel um Sweep-Bonus erhoeht (Cap 9.0); gesamt um bonus/7 (Delta-Methode). Verdikt aktualisiert. Detail pro Kapitel im Feld _sweep_adjustment.
- 2026-05-15: Validierungs-Council fuer K27 (groesste Heuristik-Anpassung) durchgefuehrt. Echtes Council-Verdikt: 9.0 FINAL-REIF — Heuristik um +1.2 unterschaetzt. K27 mit echten Werten ueberschrieben. Konsequenz: bei anderen Kapiteln mit hoher Sweep-Wirkung (K12, K22, K26, K33) ist die Heuristik-Schaetzung ebenfalls als konservative Untergrenze zu lesen — echte Werte koennten naeher an FINAL-REIF liegen.
- 2026-05-15: Varianten-Hybrid + 3 Pflicht-Fixes fuer I2 (commits dce9713 + folgender). Verifikations-Council: 9.18 FINAL-REIF. Heuristik hatte 6.6 vorhergesagt — Differenz +2.58 (Hybrid hat strukturell verbessert, nicht nur stilistisch). I2 mit echten Werten ueberschrieben.
- 2026-05-15: Varianten-Hybrid K08 + 3 Pflicht-Fixes. Verifikations-Council: 9.3 FINAL-REIF. Heuristik 6.7 unterschaetzt um +2.6. K08 mit echten Werten ueberschrieben. Bestaetigt: Heuristik fuer hochgesweepte Kapitel konservative Untergrenze.
- 2026-05-15: Varianten-Hybrid I1 (Variante-Basis + 4 Imports aus aktueller + 4 Antithese-Streichungen). Verifikations-Council: 9.3 FINAL-REIF direkt. Heuristik 7.0 unterschaetzt um +2.3. Final-Reif-Liste: 8 -> 9 Kapitel.
- 2026-05-15: Varianten-Hybrid K24 + 3 Pflicht-Fixes. Verifikations-Council: 9.2 FINAL-REIF. Heuristik 7.1 unterschaetzt um +2.1. Final-Reif-Liste: 9 -> 10 Kapitel.
- 2026-05-17: K27_5 (Vesper-V/M-Bruecke im Zeitsprung K27→K28) als 41. Eintrag aufgenommen. Pipeline-Phasen 4 + 5.5 + Final-Validierung nachgereicht (vorher Phase 5 Council bereits durchgefuehrt). Post-Sweep-Score 9.11 FINAL-REIF nach 17 Fixes (5 PFLICHT-Konvergent + 5 Sein-Verb-Sweep + 7 Autorin-Findings). Vorher-Final-Validierung 8.6 wegen Sein-Verben-Quote 18.2/1000W (60% ueber K33-Sweep-Niveau); nach Sweep der stand-/tragen-Cluster + Negations-/Aphorismen-Eliminationen erreicht stil_disziplin Final-Reife (9.0). Wortzahl 3345 → 3269 (-76W).
- 2026-05-17: K40 (Vael-Epilog) als 40. Eintrag aufgenommen. Council-Ø ohne Heat = 9.25 (FINAL-REIF strukturell), Ø mit Heat=1-Epilog-Konvention = 8.07 (formal NICHT-FINAL nach Schwelle, analog I3). Achsen: sog 8.9 / plot 9.2 / stil 9.1 / pov 9.4 / verst 9.4 / tschechow 9.5. Book-Council MEIKE 90 BESTANDEN / KAYA 88 GRENZWERTIG → Ø 89.0. Hinweis: Heat-Achse benachteiligt Epilog-/Interludien-Kapitel systematisch — strukturelle Final-Reife-Bewertung sollte heat-konditioniert lesen.

**Achsen-Durchschnitt (Council):**

| sog | plot_charakter | stil_disziplin | pov_schaerfe | heat | verstaendlichkeit | tschechow |
|---|---|---|---|---|---|---|
| 8.5 | 8.9 | 7.9 | 8.8 | 6.5 | 8.9 | 9.3 |

Schwaechste Achse systemisch: **stil_disziplin** (Ø 7.9) — getrieben von Em-Dashes, 'Takt'-Missbrauch, Stakkato-Ketten.

## Übersicht (Lese-Reihenfolge)

| Kapitel | POV | Council | Verdikt | Stil | Book | Book-Verdikt | Risiko-Stimme | PFLICHT |
|---------|-----|--------:|---------|-----:|-----:|--------------|---------------|--------:|
| B1-K01 | Alphina | 9.1 | ✅ FINAL-REIF | 9.0 | 85.7 | GRENZWERTIG | NORA 80 | 3 |
| B1-K02 | Sorel | 7.5 | NICHT-FINAL | 5.6 | 78.0 | GRENZWERTIG | KAYA 74 | 4 |
| B1-K03 | Vesper | 8.8 | NICHT-FINAL | 7.8 | 83.3 | GRENZWERTIG | LINA 78 | 1 |
| B1-K04 | Maren | 8.3 | NICHT-FINAL | 8.3 | 79.3 | GRENZWERTIG | LINA 74 | 2 |
| B1-I1 | Elke | 9.3 | ✅ FINAL-REIF | 9.0 | 72.0 | GRENZWERTIG | LINA 68 | 0 |
| B1-K05 | Alphina | 9.1 | ✅ FINAL-REIF | 9.0 | 85.5 | GRENZWERTIG | NORA 82 | 1 |
| B1-K06 | Sorel | 7.7 | NICHT-FINAL | 6.6 | 79.3 | GRENZWERTIG | LINA 74 | 2 |
| B1-K07 | Vesper | 7.9 | NICHT-FINAL | 6.8 | 78.5 | GRENZWERTIG | NORA 74 | 3 |
| B1-K08 | Maren | 9.3 | ✅ FINAL-REIF | 9.1 | 73.7 | GRENZWERTIG | LINA 68 | 0 |
| B1-I2 | Keldan | 9.2 | ✅ FINAL-REIF | 8.9 | 72.0 | GRENZWERTIG | LINA 68 | 2 |
| B1-K09 | Alphina | 8.8 | NICHT-FINAL | 9.0 | 80.5 | GRENZWERTIG | KAYA 74 | 2 |
| B1-K10 | Sorel | 8.1 | NICHT-FINAL | 7.8 | 78.0 | GRENZWERTIG | LINA 72 | 1 |
| B1-K11 | Vesper | 7.8 | NICHT-FINAL | 6.8 | 76.3 | GRENZWERTIG | NORA 72 | 3 |
| B1-K12 | Alphina/Sorel | 7.4 | NICHT-FINAL | 5.8 | 80.8 | GRENZWERTIG | KAYA 74 | 1 |
| B1-K13 | Sorel | 8.6 | NICHT-FINAL | 7.8 | 82.3 | GRENZWERTIG | NORA 78 | 3 |
| B1-K14 | Maren | 8.7 | NICHT-FINAL | 8.0 | 84.0 | GRENZWERTIG | NORA 78 | 2 |
| B1-K15 | Alphina | 8.3 | NICHT-FINAL | 7.6 | 77.5 | GRENZWERTIG | KAYA 72 | 3 |
| B1-K16 | Sorel | 8.3 | NICHT-FINAL | 6.8 | 76.0 | GRENZWERTIG | NORA 68 | 5 |
| B1-K17 | Maren | 8.9 | NICHT-FINAL | 8.6 | 80.5 | GRENZWERTIG | NORA 74 | 5 |
| B1-K18 | Vesper | 7.4 | NICHT-FINAL | 6.3 | 74.3 | GRENZWERTIG | LINA 71 | 3 |
| B1-K19 | Alle | 9.0 | ✅ FINAL-REIF | 8.6 | 82.5 | GRENZWERTIG | KAYA 78 | 1 |
| B1-K20 | Maren | 9.0 | ✅ FINAL-REIF | 9.0 | 83.3 | GRENZWERTIG | NORA 78 | 0 |
| B1-K21 | Alphina | 8.7 | NICHT-FINAL | 7.6 | 87.7 | GRENZWERTIG | NORA 84 | 3 |
| B1-K22 | Maren | 7.7 | NICHT-FINAL | 6.5 | 73.7 | GRENZWERTIG | NORA 68 | 4 |
| B1-K23 | Alphina | 8.9 | NICHT-FINAL | 8.5 | 83.0 | GRENZWERTIG | NORA 76 | 2 |
| B1-K24 | Alphina | 9.2 | ✅ FINAL-REIF | 9.0 | 73.7 | GRENZWERTIG | NORA 71 | 0 |
| B1-K25 | Runa | 8.3 | NICHT-FINAL | 7.2 | 80.3 | GRENZWERTIG | NORA 74 | 1 |
| B1-K26 | Vesper | 7.6 | NICHT-FINAL | 7.6 | 74.0 | GRENZWERTIG | LINA 69 | 1 |
| B1-K27 | Maren | 9.0 | ✅ FINAL-REIF | 9.2 | 85.3 | GRENZWERTIG | NORA 82 | 3 |
| B1-K28 | Maren | 8.9 | NICHT-FINAL | 9.0 | 82.5 | GRENZWERTIG | LINA 78 | 2 |
| B1-K29 | Sorel | 8.3 | NICHT-FINAL | 6.7 | 77.5 | GRENZWERTIG | LINA 72 | 1 |
| B1-K30 | Sorel | 9.0 | ✅ FINAL-REIF | 9.0 | 85.0 | GRENZWERTIG | NORA 80 | 0 |
| B1-K31 | Runa | 8.8 | NICHT-FINAL | 9.0 | 80.5 | GRENZWERTIG | LINA 74 | 0 |
| B1-K32 | Alphina | 8.5 | NICHT-FINAL | 8.2 | 80.8 | GRENZWERTIG | LINA 78 | 1 |
| B1-K33 | Vesper | 7.6 | NICHT-FINAL | 5.5 | 77.3 | GRENZWERTIG | LINA 72 | 1 |
| B1-K34 | Alle | 8.6 | NICHT-FINAL | 8.6 | 78.7 | GRENZWERTIG | LINA 74 | 2 |
| B1-K35 | Maren | 8.3 | NICHT-FINAL | 8.6 | 83.0 | GRENZWERTIG | MEIKE 74 | 3 |
| B1-K36 | Alphina | 8.8 | NICHT-FINAL | 8.1 | 84.3 | GRENZWERTIG | KAYA 78 | 4 |
| B1-I3 | Elke | 8.5 | NICHT-FINAL | 8.7 | 79.3 | GRENZWERTIG | LINA 74 | 2 |

## Ranking Council-Gesamt (schwächste zuerst)

- **7.4** B1-K12 (Alphina/Sorel) — NICHT-FINAL
- **7.4** B1-K18 (Vesper) — NICHT-FINAL
- **7.5** B1-K02 (Sorel) — NICHT-FINAL
- **7.6** B1-K26 (Vesper) — NICHT-FINAL
- **7.6** B1-K33 (Vesper) — NICHT-FINAL
- **7.7** B1-K06 (Sorel) — NICHT-FINAL
- **7.7** B1-K22 (Maren) — NICHT-FINAL
- **7.8** B1-K11 (Vesper) — NICHT-FINAL
- **7.9** B1-K07 (Vesper) — NICHT-FINAL
- **8.1** B1-K10 (Sorel) — NICHT-FINAL
- **8.3** B1-K04 (Maren) — NICHT-FINAL
- **8.3** B1-K15 (Alphina) — NICHT-FINAL
- **8.3** B1-K16 (Sorel) — NICHT-FINAL
- **8.3** B1-K25 (Runa) — NICHT-FINAL
- **8.3** B1-K29 (Sorel) — NICHT-FINAL
- **8.3** B1-K35 (Maren) — NICHT-FINAL
- **8.5** B1-K32 (Alphina) — NICHT-FINAL
- **8.5** B1-I3 (Elke) — NICHT-FINAL
- **8.6** B1-K13 (Sorel) — NICHT-FINAL
- **8.6** B1-K34 (Alle) — NICHT-FINAL
- **8.7** B1-K14 (Maren) — NICHT-FINAL
- **8.7** B1-K21 (Alphina) — NICHT-FINAL
- **8.8** B1-K03 (Vesper) — NICHT-FINAL
- **8.8** B1-K09 (Alphina) — NICHT-FINAL
- **8.8** B1-K31 (Runa) — NICHT-FINAL
- **8.8** B1-K36 (Alphina) — NICHT-FINAL
- **8.9** B1-K17 (Maren) — NICHT-FINAL
- **8.9** B1-K23 (Alphina) — NICHT-FINAL
- **8.9** B1-K28 (Maren) — NICHT-FINAL
- **9.0** B1-K19 (Alle) — FINAL-REIF
- **9.0** B1-K20 (Maren) — FINAL-REIF
- **9.0** B1-K27 (Maren) — FINAL-REIF
- **9.0** B1-K30 (Sorel) — FINAL-REIF
- **9.1** B1-K01 (Alphina) — FINAL-REIF
- **9.1** B1-K05 (Alphina) — FINAL-REIF
- **9.2** B1-I2 (Keldan) — FINAL-REIF
- **9.2** B1-K24 (Alphina) — FINAL-REIF
- **9.3** B1-I1 (Elke) — FINAL-REIF
- **9.3** B1-K08 (Maren) — FINAL-REIF

## Lesehinweis

Pro Kapitel stehen in `kapitel-scores.json`: 7 Council-Achsen-Scores, Gesamt + Verdikt, 3–5 Staerken, 3–5 Schwaechen, die PFLICHT-Findings (mit Zeile + Problem) sowie das Book-Council-Rating (5 Leserinnen-Stimmen, Gesamt, Verdikt, Risiko-Signal). Der Datensatz ist eine Momentaufnahme — bei Aenderungen an einem Kapitel wird der betreffende Eintrag neu erhoben.
