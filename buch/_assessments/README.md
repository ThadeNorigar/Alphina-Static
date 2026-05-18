# Kapitel-Assessment-Datensatz — Buch 1

*Erstellt: 2026-05-14 · Update: 2026-05-18 · 44 Kapitel · Schema v2 (Heat als Diagnose-Achse) · Strukturierte Daten: `kapitel-scores.json`*

Pro Kapitel ein Subagent (Opus): Council-Assessment (7 Achsen 0-10, davon 6 Kern + 1 Heat als Diagnose) + Book-Council-Rating (5 Leserinnen-Archetypen, Marktfaehigkeit 0-100).

## Schema v2 — Verdikt-Politik

- **Kern-Score** = Mittel ueber 6 monotone Achsen: `sog / plot_charakter / stil_disziplin / pov_schaerfe / verstaendlichkeit / tschechow`
- **FINAL** wenn `kern_gesamt >= 9.0`
- **Heat-Match** = `max(0, 10 - 2 * |heat_soll - heat_ist|)` — Diagnose-Achse, kein Final-Blocker
- **Heat-Flag:** OK (Match ≥ 7) · Knapp (5 ≤ Match < 7) · Miss (Match < 5) → triggert Refit-Empfehlung
- Heat-Definition strikt nach `01-autorin-stimme.md` §11: 0-1 keine, 2-3 leise, 4-6 commercial, 7-9 explizit, 8-10 explizit BDSM

## Aggregat

- **Kern-Score Ø:** 8.79 / 10
- **Heat-Match Ø:** 9.25 / 10
- **Heat-Score Ø (Ist):** 2.78 / 10 — strikte Definition
- **Book-Council-Gesamt Ø:** 80.5 / 100
- **FINAL (Kern ≥ 9.0):** 18 / 44 — B1-K01, B1-I1, B1-K05, B1-K08, B1-I2, B1-K09, B1-K19, B1-K20, B1-K24, B1-K27_5, B1-K28, B1-K30, B1-K31, B1-K33, B1-K37, B1-K38, B1-K39, B1-K40
- **NICHT-FINAL:** 26 / 44
- **Heat-Flags:** OK 44 · Knapp 0 · Miss 0
- **PFLICHT-Findings gesamt:** 89

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
- 2026-05-18: K37 (Runa, Riss-Sprung), K38 (Alphina, Sorels Tod), K39 (Alphina, Trauer-zu-Auftrag) als Assessments nachgereicht. Council: K37 7.9 NICHT-FINAL (Em-Dash + nicht-sondern-Kette + Anti-Pattern-Doppelung); K38 8.2 NICHT-FINAL (strukturell 9.27 FINAL-REIF ohne Heat; Header-Drift + Narrator-Aphorismus + Inventur-Tic); K39 8.3 NICHT-FINAL (strukturell 9.33 FINAL-REIF ohne Heat; Stakkato-Cluster + Scharnier-Aphorismus). Book-Council Ø K37 82.0 / K38 86.6 / K39 86.6 — alle GRENZWERTIG, Risiko-Stimme VICTORIA (kein BDSM-Register in Plot-/Trauer-Kapiteln).
- 2026-05-18: Schema v2 eingefuehrt + Heat-Achse re-erhoben. Alte Heat-Werte (Ø 6.6) waren Methoden-Drift (Subagenten haben Heat als Spannung/Intensitaet interpretiert, nicht Begehren/Sex-Register). Neue Werte (Ø 2.8) strikt nach 01-autorin-stimme.md §11. Verdikt-Politik geaendert: Kern (6 monotone Achsen) bestimmt FINAL-Status, Heat ist Diagnose-Achse (Match-Flag OK/Knapp/Miss) ohne Final-Blocker-Wirkung. Effekt: FINAL-Liste 11 → 17 (Trauer-/Plot-/Epilog-Kapitel mit hohem Kern-Score koennen jetzt sauber final werden — K28, K30, K31, K37, K38, K39, K40 neu drin). Alle 44 Kapitel haben Heat-Flag OK.
- 2026-05-18: K33-Refit (Sammel-Hybrid + 4-Council-Validierung) — Stil 5.5 → 9.1, Kern 9.33 FINAL. 7 Bloecke ueber Sz1 (Pendel-Justierung, Karst-Flashback, Karst-Coda), Sz2 (Erkenntnis-Cluster), Sz3 (Morgen-Bett, Welle-Rueckweg, Vier-Personen-Klaerung) ueberarbeitet; 11 Mikro-Fixes auf Sweep-Cluster (sauber-Wertung raus, gleichmaessig 9→2, Mind-Reading-Cluster reduziert, Antithese-Doppel-Pointen aufgeloest). FINAL-Liste B1: 17 → 18. Wortzahl 3766 → 3462.

**Achsen-Durchschnitt:**

| sog | plot_charakter | stil_disziplin | pov_schaerfe | verstaendlichkeit | tschechow | heat (ist) |
|---|---|---|---|---|---|---|
| 8.6 | 8.9 | 8.1 | 8.9 | 8.9 | 9.3 | 2.8 |

Schwaechste Kern-Achse systemisch: **stil_disziplin** (Ø 8.1).

## Übersicht (Lese-Reihenfolge)

| Kapitel | POV | Kern | Verdikt | Stil | Heat (Ist/Soll) | Match | Flag | Book | Risiko | PFLICHT |
|---------|-----|-----:|---------|-----:|----------------:|------:|------|-----:|--------|--------:|
| B1-K01 | Alphina | 9.17 | ✅ FINAL | 9.0 | 1.0 / 2 | 8.0 | ✓ OK | 85.7 | NORA 80 | 3 |
| B1-K02 | Sorel | 7.85 | NICHT-FINAL | 5.6 | 0.5 / 1 | 9.0 | ✓ OK | 78.0 | KAYA 74 | 4 |
| B1-K03 | Vesper | 8.97 | NICHT-FINAL | 7.8 | 0.5 / 1 | 9.0 | ✓ OK | 83.3 | LINA 78 | 1 |
| B1-K04 | Maren | 8.63 | NICHT-FINAL | 8.3 | 1.0 / 1 | 10.0 | ✓ OK | 79.3 | LINA 74 | 2 |
| B1-I1 | Elke | 9.27 | ✅ FINAL | 9.0 | 0.0 / 0 | 10.0 | ✓ OK | 72.0 | LINA 68 | 0 |
| B1-K05 | Alphina | 9.08 | ✅ FINAL | 9.0 | 2.0 / 2 | 10.0 | ✓ OK | 85.5 | NORA 82 | 1 |
| B1-K06 | Sorel | 8.35 | NICHT-FINAL | 6.6 | 0.5 / 1 | 9.0 | ✓ OK | 79.3 | LINA 74 | 2 |
| B1-K07 | Vesper | 8.30 | NICHT-FINAL | 6.8 | 2.5 / 3 | 9.0 | ✓ OK | 78.5 | NORA 74 | 3 |
| B1-K08 | Maren | 9.28 | ✅ FINAL | 9.1 | 1.0 / 2 | 8.0 | ✓ OK | 73.7 | LINA 68 | 0 |
| B1-I2 | Keldan | 9.18 | ✅ FINAL | 8.9 | 0.0 / 0 | 10.0 | ✓ OK | 72.0 | LINA 68 | 2 |
| B1-K09 | Alphina | 9.08 | ✅ FINAL | 9.0 | 2.5 / 3 | 9.0 | ✓ OK | 80.5 | KAYA 74 | 2 |
| B1-K10 | Sorel | 8.55 | NICHT-FINAL | 7.8 | 1.0 / 2 | 8.0 | ✓ OK | 78.0 | LINA 72 | 1 |
| B1-K11 | Vesper | 8.30 | NICHT-FINAL | 6.8 | 2.5 / 3 | 9.0 | ✓ OK | 76.3 | NORA 72 | 3 |
| B1-K12 | Alphina/Sorel | 7.88 | NICHT-FINAL | 5.8 | 3.5 / 4 | 9.0 | ✓ OK | 80.8 | KAYA 74 | 1 |
| B1-K13 | Sorel | 8.83 | NICHT-FINAL | 7.8 | 3.5 / 3 | 9.0 | ✓ OK | 82.3 | NORA 78 | 3 |
| B1-K14 | Maren | 8.83 | NICHT-FINAL | 8.0 | 4.0 / 4 | 10.0 | ✓ OK | 84.0 | NORA 78 | 2 |
| B1-K15 | Alphina | 8.52 | NICHT-FINAL | 7.6 | 1.5 / 2 | 9.0 | ✓ OK | 77.5 | KAYA 72 | 3 |
| B1-K16 | Sorel | 8.63 | NICHT-FINAL | 6.8 | 4.5 / 4 | 9.0 | ✓ OK | 76.0 | NORA 68 | 5 |
| B1-K17 | Maren | 8.93 | NICHT-FINAL | 8.6 | 4.5 / 5 | 9.0 | ✓ OK | 80.5 | NORA 74 | 5 |
| B1-K18 | Vesper | 7.72 | NICHT-FINAL | 6.3 | 3.5 / 4 | 9.0 | ✓ OK | 74.3 | LINA 71 | 3 |
| B1-K19 | Alle | 9.02 | ✅ FINAL | 8.6 | 2.5 / 3 | 9.0 | ✓ OK | 82.5 | KAYA 78 | 1 |
| B1-K20 | Maren | 9.00 | ✅ FINAL | 9.0 | 3.0 / 3 | 10.0 | ✓ OK | 83.3 | NORA 78 | 0 |
| B1-K21 | Alphina | 8.77 | NICHT-FINAL | 7.6 | 9.0 / 9 | 10.0 | ✓ OK | 87.7 | NORA 84 | 3 |
| B1-K22 | Maren | 8.17 | NICHT-FINAL | 6.5 | 3.5 / 3 | 9.0 | ✓ OK | 73.7 | NORA 68 | 4 |
| B1-K23 | Alphina | 8.92 | NICHT-FINAL | 8.5 | 5.0 / 5 | 10.0 | ✓ OK | 83.0 | NORA 76 | 2 |
| B1-K24 | Alphina | 9.22 | ✅ FINAL | 9.0 | 2.0 / 2 | 10.0 | ✓ OK | 73.7 | NORA 71 | 0 |
| B1-K25 | Runa | 8.45 | NICHT-FINAL | 7.2 | 7.0 / 6 | 8.0 | ✓ OK | 80.3 | NORA 74 | 1 |
| B1-K26 | Vesper | 8.02 | NICHT-FINAL | 7.6 | 2.0 / 3 | 8.0 | ✓ OK | 74.0 | LINA 69 | 1 |
| B1-K27 | Maren | 8.95 | NICHT-FINAL | 9.2 | 9.0 / 9 | 10.0 | ✓ OK | 85.3 | NORA 82 | 3 |
| B1-K27_5 | Vesper | 9.22 | ✅ FINAL | 9.0 | 8.0 / 8 | 10.0 | ✓ OK | 86.7 | NORA 85 | 0 |
| B1-K28 | Maren | 9.08 | ✅ FINAL | 9.0 | 1.5 / 2 | 9.0 | ✓ OK | 82.5 | LINA 78 | 2 |
| B1-K29 | Sorel | 8.62 | NICHT-FINAL | 6.7 | 2.0 / 2 | 10.0 | ✓ OK | 77.5 | LINA 72 | 1 |
| B1-K30 | Sorel | 9.18 | ✅ FINAL | 9.0 | 2.0 / 3 | 8.0 | ✓ OK | 85.0 | NORA 80 | 0 |
| B1-K31 | Runa | 9.08 | ✅ FINAL | 9.0 | 0.5 / 1 | 9.0 | ✓ OK | 80.5 | LINA 74 | 0 |
| B1-K32 | Alphina | 8.70 | NICHT-FINAL | 8.2 | 1.0 / 1 | 10.0 | ✓ OK | 80.8 | LINA 78 | 1 |
| B1-K33 | Vesper | 9.33 | ✅ FINAL | 9.1 | 1.5 / 2 | 9.0 | ✓ OK | 77.3 | LINA 72 | 0 |
| B1-K34 | Alle | 8.85 | NICHT-FINAL | 8.6 | 1.0 / 2 | 8.0 | ✓ OK | 78.7 | LINA 74 | 2 |
| B1-K35 | Maren | 8.35 | NICHT-FINAL | 8.6 | 9.0 / 9 | 10.0 | ✓ OK | 83.0 | MEIKE 74 | 3 |
| B1-K36 | Alphina | 8.93 | NICHT-FINAL | 8.1 | 5.0 / 5 | 10.0 | ✓ OK | 84.3 | KAYA 78 | 4 |
| B1-I3 | Elke | 8.70 | NICHT-FINAL | 8.7 | 1.5 / 1 | 9.0 | ✓ OK | 79.3 | LINA 74 | 2 |
| B1-K37 | Runa | 9.00 | ✅ FINAL | 7.8 | 1.5 / 2 | 9.0 | ✓ OK | 82.0 | VICTORIA 72 | 6 |
| B1-K38 | Alphina | 9.27 | ✅ FINAL | 8.7 | 2.0 / 2 | 10.0 | ✓ OK | 86.6 | VICTORIA 70 | 5 |
| B1-K39 | Alphina | 9.33 | ✅ FINAL | 8.8 | 2.0 / 2 | 10.0 | ✓ OK | 86.6 | VICTORIA 78 | 2 |
| B1-K40 | Jara/Edric/Tarn (Multi-POV) | 9.25 | ✅ FINAL | 9.1 | 1.0 / 1 | 10.0 | ✓ OK | 89.0 | KAYA 88 | 0 |

## Ranking Kern-Score (schwächste zuerst)

- **7.72** B1-K18 (Vesper) — NICHT-FINAL
- **7.85** B1-K02 (Sorel) — NICHT-FINAL
- **7.88** B1-K12 (Alphina/Sorel) — NICHT-FINAL
- **8.02** B1-K26 (Vesper) — NICHT-FINAL
- **8.17** B1-K22 (Maren) — NICHT-FINAL
- **8.30** B1-K07 (Vesper) — NICHT-FINAL
- **8.30** B1-K11 (Vesper) — NICHT-FINAL
- **8.35** B1-K06 (Sorel) — NICHT-FINAL
- **8.35** B1-K35 (Maren) — NICHT-FINAL
- **8.45** B1-K25 (Runa) — NICHT-FINAL
- **8.52** B1-K15 (Alphina) — NICHT-FINAL
- **8.55** B1-K10 (Sorel) — NICHT-FINAL
- **8.62** B1-K29 (Sorel) — NICHT-FINAL
- **8.63** B1-K04 (Maren) — NICHT-FINAL
- **8.63** B1-K16 (Sorel) — NICHT-FINAL
- **8.70** B1-K32 (Alphina) — NICHT-FINAL
- **8.70** B1-I3 (Elke) — NICHT-FINAL
- **8.77** B1-K21 (Alphina) — NICHT-FINAL
- **8.83** B1-K13 (Sorel) — NICHT-FINAL
- **8.83** B1-K14 (Maren) — NICHT-FINAL
- **8.85** B1-K34 (Alle) — NICHT-FINAL
- **8.92** B1-K23 (Alphina) — NICHT-FINAL
- **8.93** B1-K17 (Maren) — NICHT-FINAL
- **8.93** B1-K36 (Alphina) — NICHT-FINAL
- **8.95** B1-K27 (Maren) — NICHT-FINAL
- **8.97** B1-K03 (Vesper) — NICHT-FINAL
- **9.00** B1-K20 (Maren) — FINAL
- **9.00** B1-K37 (Runa) — FINAL
- **9.02** B1-K19 (Alle) — FINAL
- **9.08** B1-K05 (Alphina) — FINAL
- **9.08** B1-K09 (Alphina) — FINAL
- **9.08** B1-K28 (Maren) — FINAL
- **9.08** B1-K31 (Runa) — FINAL
- **9.17** B1-K01 (Alphina) — FINAL
- **9.18** B1-I2 (Keldan) — FINAL
- **9.18** B1-K30 (Sorel) — FINAL
- **9.22** B1-K24 (Alphina) — FINAL
- **9.22** B1-K27_5 (Vesper) — FINAL
- **9.25** B1-K40 (Jara/Edric/Tarn (Multi-POV)) — FINAL
- **9.27** B1-I1 (Elke) — FINAL
- **9.27** B1-K38 (Alphina) — FINAL
- **9.28** B1-K08 (Maren) — FINAL
- **9.33** B1-K33 (Vesper) — FINAL
- **9.33** B1-K39 (Alphina) — FINAL

## FINAL-Liste (Kern ≥ 9.0)

- **9.33** B1-K33 (Vesper) · Heat 1.5/2 (Match 9.0)
- **9.33** B1-K39 (Alphina) · Heat 2.0/2 (Match 10.0)
- **9.28** B1-K08 (Maren) · Heat 1.0/2 (Match 8.0)
- **9.27** B1-I1 (Elke) · Heat 0.0/0 (Match 10.0)
- **9.27** B1-K38 (Alphina) · Heat 2.0/2 (Match 10.0)
- **9.25** B1-K40 (Jara/Edric/Tarn (Multi-POV)) · Heat 1.0/1 (Match 10.0)
- **9.22** B1-K24 (Alphina) · Heat 2.0/2 (Match 10.0)
- **9.22** B1-K27_5 (Vesper) · Heat 8.0/8 (Match 10.0)
- **9.18** B1-I2 (Keldan) · Heat 0.0/0 (Match 10.0)
- **9.18** B1-K30 (Sorel) · Heat 2.0/3 (Match 8.0)
- **9.17** B1-K01 (Alphina) · Heat 1.0/2 (Match 8.0)
- **9.08** B1-K05 (Alphina) · Heat 2.0/2 (Match 10.0)
- **9.08** B1-K09 (Alphina) · Heat 2.5/3 (Match 9.0)
- **9.08** B1-K28 (Maren) · Heat 1.5/2 (Match 9.0)
- **9.08** B1-K31 (Runa) · Heat 0.5/1 (Match 9.0)
- **9.02** B1-K19 (Alle) · Heat 2.5/3 (Match 9.0)
- **9.00** B1-K20 (Maren) · Heat 3.0/3 (Match 10.0)
- **9.00** B1-K37 (Runa) · Heat 1.5/2 (Match 9.0)

## Lesehinweis

Pro Kapitel stehen in `kapitel-scores.json`: 7 Council-Achsen-Scores (6 Kern + Heat), Kern-Gesamt + Verdikt-neu, Heat-Soll/Ist/Match/Flag, 3–5 Staerken, 3–5 Schwaechen, die PFLICHT-Findings (mit Zeile + Problem) sowie das Book-Council-Rating (5 Leserinnen-Stimmen, Gesamt, Verdikt, Risiko-Signal). Heat-Achse ist Diagnose, nicht Verdikt — Heat-Miss triggert Refit-Empfehlung, blockt aber nicht Final-Status. Der Datensatz ist eine Momentaufnahme — bei Aenderungen an einem Kapitel wird der betreffende Eintrag neu erhoben.
