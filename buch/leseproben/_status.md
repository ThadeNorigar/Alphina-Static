# Leseproben — Status & Pipeline-Tracker

**Stand:** 2026-05-03 · **Master-Pipeline:** sequenziell pro Probe, Subagent-getrieben.

## Pipeline pro Probe (4 Schritte)

1. **Neuschrieb-Subagent** schreibt Probe komplett neu auf Basis der Referenzquellen-Hebel + Master-Files (Stilregeln, Autor-Stimme, Konkretheit, Positioning, POV-Dossier). Output: `_neuschrieb-{NN}.md` (temporär neben dem Original).
2. **Autor-Abnahme des Neuschriebs.** Korrekturen → zurück zu Schritt 1. OK → weiter.
3. **Refit-Pipeline + Vergleich** (5 parallele Subagenten auf Neuschrieb):
   - Sprach-TÜV
   - Verquastungs-Detektor
   - Konsistenz/Logik
   - Genre-Leserin (passend zu Heat-Level)
   - **Vergleichs-Subagent**: kritische Analyse alt vs neu — welche Quellen-Hebel angekommen, welche fehlen, welche Original-Stärken im Neuschrieb verloren
   - Findings strikt nach `buch/_findings-format.md` (Block-Format mit Vorher/Nachher und Kontext)
4. **Final-Abnahme.** Autor entscheidet pro Finding. Findings einarbeiten → Original ersetzen → `_neuschrieb-{NN}.md` löschen → Status ✅.

**Sammel-Commit + Deploy** am Ende aller 35 Proben (nicht zwischendurch).

**Hauptsession-Disziplin:** Alle Lese-/Schreib-Last in Subagenten. Hauptsession synthetisiert nur — keine Volltext-Reads von Quellen oder Mastern in der Hauptsession.

## Quellen-Anker pro Probe

| # | Probe | POV | Heat | Primär | Sekundär |
|---|---|---|---|---|---|
| 01 | Banter Alphina/Sorel | Alphina | leise | RY | JM |
| 02 | Erster Kuss | Alphina | commercial | RY | JM |
| 03 | Heat Alphina/Sorel | Alphina | explizit non-BDSM | JM | RY |
| 04 | BDSM-Alltag Vesper/Maren | Maren | leise | Réage | Rampling, **SLY** |
| 05 | BDSM-Szene explizit | Maren | explizit BDSM | Réage | Rampling, **SLY** |
| 06 | Aftercare-Miniatur | Vesper | ruhig | Rampling | **SLY** |
| 07 | Antagonist Varen | Alphina | Drohung | JM | (Robert fehlt) |
| 08 | Magie-Kontrollverlust | Alphina | Action | RY + SLY | — |
| 09 | Welt Vael warm (Werft) | Maren | keine | JM | — |
| 10 | Welt Vael kalt (Archiv) | Vesper | keine | JM | — |
| 11 | Moragh-Ankunft | Alphina | Drohung | JM | SLY |
| 12 | Gruppenszene Tension | wechselnd | leise | JM | RY |
| 13 | Krieg/Schlachtfeld | Alphina (B2) | Gewalt | SLY | (Kuang fehlt) |
| 14 | Völkermord-Täter-POV | Alphina (B2) | Gewalt | SLY | (Kuang fehlt) |
| 15 | Post-Krieg-Ruine | Alphina (B2) | Drohung | SLY | — |
| 16 | Biotech-Dystopie | Nyr (B3) | Gewalt | SLY | (Pierce Brown fehlt) |
| 17 | Körper-Mutilation | Alphina (B3) | Gewalt | SLY | Réage |
| 18 | Fehlurteil-Schuld | Alphina (B3) | Trauer | (Morrison fehlt) | SLY |
| 19 | Narbige Ruhe | Alphina (B3) | keine | (Morrison fehlt) | RY |
| 20 | Captivity-Folter | Alphina | Gewalt | SLY | — |
| 21 | Bund-Kultur | Alphina | keine | JM | — |
| 22 | Thar-Kultur | wechselnd | keine | JM | — |
| 23 | Velmar-Kultur | Vesper | keine | JM | — |
| 24 | Alphina/Runa FWB | Alphina | commercial | RY | JM |
| 25 | Vesper/Nyr Thar-Register | Vesper | leise BDSM | Réage | Rampling, **SLY** |
| 26 | Alphina/Varen Machtpakt | Alphina | Drohung | JM | Réage, **SLY** |
| 27 | Alphina-Sub/Vesper-Dom | Alphina | explizit BDSM | Réage | Rampling, **SLY** |
| 28 | Sorel-Tod-Moment | Alphina | Trauer | JM | RY | ⏳ TODO Stein-Bruch-Mechanik korrigieren (Pflanzen DURCH Stein, nicht Stein-direkt) — Memory `project_stein_quellen_pflanzen_resonanz.md` |
| 29 | Portal-Öffnung Ritual | Alphina | Drohung | JM | — |
| 30 | Verwüster Vael/Marens Tod | Maren | Gewalt | SLY | JM |
| 31 | Varen-Reveal-Dialog | Alphina | Drohung | JM | RY |
| 32 | Schemen-Angriff | Alphina | Gewalt | SLY | JM |
| 33 | Talven-Blutmagie | Alphina | Gewalt | SLY | — |
| 34 | Runa-Verzeihung | Alphina | Trauer | RY | — |
| 35 | Folter brutal | Alphina | Gewalt | SLY | — |

**SLY-Sekundär-Direktive (User 2026-05-03):** SLY ist Sekundärquelle bei allen BDSM-Stellen (04, 05, 06, 25, 27) und bei Captivity-Power-Dynamik (26). Begründung: SLYs Körperteil-Subjekt-Präzision + Material-Funktionsname tragen den dunkleren Untergrund, der unter dem BDSM-Register sichtbar bleiben soll. Réage allein ist klinisch — SLY bringt die Härte.

## Status-Übersicht

| # | Status | Version | Score | Datum | Notiz |
|---|---|---|---|---|---|
| 01 | ✅ erledigt | v2 | LINA 100% | 2026-05-02 | Pilot — Top-3-Übernahme: Sorel-Körper, Welt-Dichte, Body-Beats. Block A + C-1 fix. |
| 02 | ✅ erledigt | v3 | LINA 100% | 2026-05-03 | Refit-Pipeline (6 Subagenten inkl. Bild-Logik/Verb-Präzision) + Vergleichs-Subagent. Block A+B+D+E-1 + 7 F-Findings. C-Stil-Vorbehalte behalten. |
| 03 | ⏳ v5 anstehend | v4 | LINA 96% | 2026-05-03 | v4 Refit-Pipeline + BDSM-Drift-Korrektur OK. **TODO v5:** Sorel-spezifische Farn-Manifestation als Modus-A-Heat-Echo ergänzen (zusätzlich zum Geissblatt-Klirren). Memory `project_alphina_heat_echo_pflanzen.md` (2026-05-03). |
| 04 | ✅ erledigt | — | (User-Direktive 2026-05-03) | — |
| 05 | ✅ erledigt | v3 | MEIKE 88-92% | 2026-05-03 | Refit-Pipeline (6 Subagenten inkl. Bild-Logik/Verb-Präzision) + Vergleichs-Subagent. Block A 7 PFLICHT + Block B 11 EMPFEHLUNG (Sweeps lag/kam/legen) + Q1-Q3 Réage-Reinform-Eingriffe. v3 User-Korrekturen: Schnur→Seil, Sehne→konkrete Anatomie, eins-eins-eins raus, Lob-Beat konkret, Bondage-Geometrie Querbalken statt Bettpfosten. |
| 06 | ⏳ offen | — | — | — |
| 07 | ⏳ offen | — | — | — |
| 08 | ✅ erledigt | — | (User-Direktive 2026-05-03) | — |
| 09 | ⏳ offen | — | — | — |
| 10 | ⏳ offen | — | — | — |
| 11 | ⏳ offen | — | — | — |
| 12 | ⏳ offen | — | — | — |
| 13–35 | ⏳ offen | — | — | — |

**Wellen-Plan:**
- **Welle 1 (Pilot 4 Proben sequenziell):** 02, 03, 05, 06 — testet Pipeline auf Romantasy-Heat + BDSM-Register
- **Welle 2:** 07, 09, 10, 11, 12 — Welt/Antagonist/Atmosphäre
- **Welle 3:** 21–24 — Kultur + Runa-FWB
- **Welle 4:** 13–20 — dunkle Register B2/B3
- **Welle 5:** 25–35 — Spezialfälle + dunkle Spitzen

## Fehlende Quellen (Material-Wünsche aus README `buch/referenzen/`)

- **Kuang** (*Poppy War*) für Krieg/Völkermord (13, 14)
- **Pierce Brown** (*Red Rising*) für Biotech-Dystopie (16)
- **Morrison** für Trauer/Schuld/narbige Ruhe (18, 19)
- **Robert** (*Neon Gods*) für Antagonist-Schärfe (07, 26)
- **Reisz** für BDSM-Alltag/Aftercare (04, 06)
- **Rampling Belinda** statt Exit to Eden für Alphina/Sorel (Vermerk im README)

Falls eine Probe auf eine fehlende Primär-Quelle angewiesen wäre: Hinweis vermerken, ggf. mit verfügbarem Sekundär-Anker durchführen, klar markieren als „ohne Primär-Anker".
