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
| 28 | Sorel-Tod-Moment | Alphina | Trauer | JM | RY | ✅ v3 Voice-Anchored Refit + Stein-Bruch-Mechanik korrigiert 2026-05-05 (Pflanzen wachsen durch organische Substanz im Moragh-Boden, brechen Stein als Konsequenz) |
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
| 03 | ✅ erledigt | v5 | LINA 96% | 2026-05-05 | v5: Sorel-spezifische Farn-Manifestation als Modus-A-Heat-Echo eingebaut (Z.60, direkt nach Geissblatt-Klirren im Klimax). Wedel aus Mauerritzen, hellgrün/jung/aufgerollt, Phototropismus-Echo K21-Voice. Geissblatt-Anker (Welt-Signatur) parallel behalten. Memory `project_alphina_heat_echo_pflanzen.md` umgesetzt. |
| 04 | ✅ erledigt | — | (User-Direktive 2026-05-03) | — |
| 05 | ✅ erledigt | v3 | MEIKE 88-92% | 2026-05-03 | Refit-Pipeline (6 Subagenten inkl. Bild-Logik/Verb-Präzision) + Vergleichs-Subagent. Block A 7 PFLICHT + Block B 11 EMPFEHLUNG (Sweeps lag/kam/legen) + Q1-Q3 Réage-Reinform-Eingriffe. v3 User-Korrekturen: Schnur→Seil, Sehne→konkrete Anatomie, eins-eins-eins raus, Lob-Beat konkret, Bondage-Geometrie Querbalken statt Bettpfosten. |
| 06 | ✅ erledigt | v3 | MEIKE 89% · Vision 91% | 2026-05-04 | Voice-Anchored Refit-Pipeline (Antislop-Layer-1 + 5 Subagenten inkl. Vision-Layer-NEU). v2 Block A 8 PFLICHT + Block B 3 EMPFEHLUNG. v3 Voice-Anchoring an Vesper-Voice-Exemplars + Antislop-Fixes (sein_verb_cluster 7→5, hatte 6→3, legte 3→2, daumen 3→2). Final Block A 1 PFLICHT (Doppelung „schwer") + Block B 4 EMPFEHLUNG (Erklär-Glosse Z.33, Daumen/Fingerkuppe-Cluster, Augenbinden-Glosse, Tempus-Fix Z.43). Konflikt-Hierarchie aktiv: Z.25 Inventur durch MEIKE-Lob in Block C. |
| 07 | ✅ erledigt | v2.1 | Vision 86% · Voice Alphina 88% | 2026-05-05 | Voice-Anchored Refit + Block-B-Politur (Daumen-Cluster 4→2, „kam"-Sprech-Tic 3→1). Antagonist Varen, Heat: Drohung. JM-Primaer (Macht-Asymmetrie, Yarros-Triade). Heat-Echo Dornenranke mit Purpurblüte. |
| 08 | ✅ erledigt | — | (User-Direktive 2026-05-03) | — |
| 09 | ✅ erledigt | v2.1 | Vision 88% · Voice Maren 88% (nach Politur) | 2026-05-05 | Voice-Anchored Refit + Block-B-Politur. Lieblingswörter ergänzt (dicht/satt/stetig — total 4×), Narrator-Glosse Z.35 gestrafft, Bild-Logik Z.37 gefixt („bitter, dünn, kalt"). Werft-Routine-Etüde mit Tschechow-Saaten (TZ-154-Anomalie, Grauwe rückwärts). |
| 10 | ✅ erledigt | v2.1 | Vision 78% · Voice Vesper 88% | 2026-05-04 | Voice-Anchored Refit-Pipeline. Welt-Vael-kalt (Karst-Werkstatt-Cold-Open + Schachturm-Tasten + Mevissen-Standuhr). Reviewer NICHT BESTANDEN → Block-A-Fixes (Drift→Abweichung, nicht-sondern raus, halb-X raus, Sein-Cluster 26→13, hatte 24→16, Anaphern). Antislop nach Fixes BESTANDEN. Tschechow-Saaten: Mevissen-Unruh zittert, Schachturm seit Karst kalt, Taschenuhr nur hier rein, Brief 4:33, Wartungsregister 1815. |
| 11 | ✅ erledigt | v2.1 | Vision 88% · Voice Alphina 92% | 2026-05-04 | Voice-Anchored Refit-Pipeline. Moragh-Ankunft, JM-Primaer (Welt-Schock Sinnes-Aufprall) + SLY-Sekundaer (Körperteil-Subjekt). Reviewer GRENZWERTIG → Block-A-Fixes (Negations-Cluster 35→24, „Sie kannte"-Triade gebrochen, „Der"-Quartett gebrochen, kannte 7→3, exakt→genau). Antislop BESTANDEN. Tschechow-Saaten: vier+1 Stengel = Sorel-Echo, Marens Wasser ohne Schale, grüner Grat, identische Tier-Rufe, Pflanzen wachsen hinter ihr. |
| 12 | ✅ erledigt | v2.2 | Vision 78% · Voice Vesper 88% | 2026-05-05 | Voice-Anchored Refit + Block-A-Fixes + Block-B-Politur. Gruppenszene Tension, POV Vesper (5 Figuren). JM-Primaer + RY-Sekundaer. v2.1: Block-A (Dash-Antithese, Substantiv-Phrasen, Anaphern, hatte 21→7, Sein-Cluster 31→21). v2.2: rechte 5→3, heute 4→2, Fensterbank 5→3. Mikro-Gesten: Lederriemen, Knie-Touch, Daumen-am-Kragen als Mieder-Echo. |
| 21 | ✅ erledigt | v2.1 | Vision 80% · Voice Alphina 90% | 2026-05-05 | Voice-Anchored Refit + Block-A-Fixes. Bund-Kultur, Alphina-POV. JM-Welt-Etüde, areligiös. Setting-Korrektur Orath → Halvaren (canon-konform). Z.55 Verquastung gefixt, hatte-Tic 5→2. Tschechow: Kreis-mit-Strich (Halvara-Kel), Schlaf-Hain mit Sorel-Baum, Verbund-Quelle, Schlag-Vokabel. Antislop BESTANDEN. |
| 22 | ✅ erledigt | v2 | Vision 84% · Voice Nyr ~78% | 2026-05-05 | Voice-Anchored Refit. Thar-Kultur, POV-Korrektur Original „wechselnd"→Single-POV Nyr (gerechtfertigt: Original sagte „pov: Nyr ODER Vesper"). Werkstatt-Setting, Kessler-Bestie. Voice-Treffer Approximation (kein nyr-voice-exemplar verfügbar). Tschechow: 7/10-Kupplung, Karath-Fahrt, Pilotin-Bestie-Bindung, Werkzeug-Nische als Thar-Code. Antislop BESTANDEN. |
| 23 | ✅ erledigt | v2.1 | Vision 84% · Voice Vesper 90% | 2026-05-05 | Voice-Anchored Refit + Block-A-Sanierung. Plot-Änderung Original (Varen-Rückblende) → Vesper-POV B3-Bindekammer (gerechtfertigt, Status-Tabelle vorgegeben). 7 PFLICHT-Fixes (Antithese, Dash-Antithese, halb-X 2×, „Zentimeter"-Anglizismus, „dachte"-Tag, Substantiv-Refrain). Sein-Cluster 30→26, Negationen 48→<26, 4 Anaphern-Kaskaden gebrochen. Namens-Korrektur Helva Drein → Helvar Drevia. Antislop BESTANDEN. Tschechow: 7 Halsbänder + Stahlring matt-violett-Anzeige, versteckter Schrank, drei-Meisterinnen-Hierarchie, violetter Iris-Stich, Karst-Standuhr-Innenfutter. |
| 24 | ✅ erledigt | v2.2 | Vision 85% · Voice Alphina 88% | 2026-05-05 | Voice-Anchored Refit + Block-A-Fixes + Glutmoos-Manifestation. Heat-Echo-Frage gelöst: Runa=Glutmoos (Modus A bei FWB-Sex). Asymmetrische Wahrnehmung — Alphina sieht rötlichen Schein und liest „warmer Stein in der Sonne", Runa fühlt vor Alphina die Wärme an Handflächen. „Bei Sorel hat die Welt geblüht. Bei Runa lag sie still." behalten (Alphina-POV-Fehl-Lesart, Subtext für Leserin). Tschechow: Brandfleck-Letternform, Druckerinnen-Schwiele, Geißblatt-Negativ (Sorel-Vergleich), Glutmoos-Polster auf Mauer. |
| 13 | ✅ erledigt | v2 | Vision 78% · Voice Alphina 88% | 2026-05-05 | Voice-Anchored Refit-Pipeline. Krieg/Schlachtfeld B2-Akt-II, Alphina-POV. SLY-Sekundaer (Koerperteil-Subjekt: Trommelfelle/Kehle, Material-Funktionsname: Kurzschwert-Schwert-Griff). **Kuang FEHLT** — als „ohne Primaer-Anker" markiert (im Frontmatter), Taeter-POV-ohne-Anaesthesie ueber SLY-Hebel + Pause-als-Wahl getragen. Antislop-Iter 2 BESTANDEN (von 8 PFLICHT/TIC nach 0). Anti-Flora-Erstmanifestation in Bund-Kontext (gruen→Purpurstaengel mit schwarzen Dornen + blutroter Bluete), Mittelfinger bleibt purpur als Disziplin-Echo. Tschechow: Bund-Kommandant-Distanz (Mantel weicht aus) als Setup B2-K29-Skepsis, „Verunreinigung"-Vokabular implizit, „Anker-Mauer" als Vael-Echo, Pause-als-Wahl als B3-Charakter-Achse-Setup. |
| 14 | ✅ erledigt | v2.1 | Vision 78% · Voice Alphina 82% | 2026-05-05 | Völkermord-Täter-POV, B2 Bekehrungs-Bogen. SLY-Primär (Kuang fehlt). Reviewer NICHT BESTANDEN → Block-A (Dash-Antithese, Negations-Cluster 16→<11, hatte 8→3, Kommandant 4→2, Erklär-Glosse). Antislop BESTANDEN. Tschechow: Idrun-Frau, „Verunreinigung"-Vokabular, Schwarz-bis-Handgelenk Eskalation. |
| 15 | ✅ erledigt | v2.1 | Vision 88% · Voice Alphina 92% | 2026-05-05 | Post-Krieg-Ruine, Heat Drohung. SLY-Primär. Reviewer NICHT BESTANDEN → Block-A (Substantiv-Phrase Em-Dash, Antithese, Sein/hatte 19→11, Negationen 16→11). Antislop BESTANDEN. Tschechow: Wurzel aus Mörtelfuge (Pflanzen-durch-Stein), Stieglitz-Erinnerung, Quellen-Tötung-Schuld, Varens Lüge offen markiert. |
| 16 | ✅ erledigt | v2.1 | Vision 78% · Voice Nyr ~78% (Approximation) | 2026-05-05 | Biotech-Dystopie B3, Nyr-POV. SLY-Primär (Pierce Brown fehlt). Reviewer NICHT BESTANDEN → Block-A (Antithese, „Resonanz" raus, Substantiv-Kette, Wulst-Cluster). Frontmatter-„Druck-Resonanz" als POV-Charakterisierung erlaubt. Tschechow: Nadel-Tracking, zwölf identische Haltungen, modulare Bodymod, Vespers Zittern, 2.500 weitere. |
| 17 | ✅ erledigt | v3 | Vision 84% · Voice Alphina 86% | 2026-05-05 | Körper-Mutilation B3 Akt IV. SLY+Réage. v2.1: Canon-Fix Maren→Runa 3× + Block-A-Fixes. v3: Mechanik-Präzisierung — Runa-Direkt-Hitze (Stufe-10, eigene Haut immun, kein Werkzeug). Z.73 „Runa bringt Feuer und Tuch" → „Runa bringt ihre Hand und ein Tuch". Hand-Geometrie kanonisch. Antislop BESTANDEN. Tschechow: Schwarze Wurzel aus Mauerritze (Anti-Flora B3), Faden unter Schlüsselbein. |
| 18 | ✅ erledigt | v2.1 | Vision 72% · Voice Alphina 78% | 2026-05-05 | Fehlurteil-Schuld B3, Heat Trauer. Morrison fehlt → SLY/Voice-Exemplars rekonstruiert. Reviewer NICHT BESTANDEN → Block-A (parallel-Tic, Doppelnegationen, Negations-Cluster 21→3, hatte 16→6, Magie-Spuk-Korrektur, Tonfolge Bass→Alt). Antislop BESTANDEN. Tschechow: Drei Stümpfe, Kamm aus Horn, Steckling-Kontrollverlust (Magie-ohne-Vorstellung). |
| 19 | ✅ erledigt | v2 | Vision 85% · Voice Alphina 88% | 2026-05-05 | Narbige Ruhe B3. Aftermath-Etüde. Morrison fehlt → RY-Sekundär. Canon-Korrekturen: Daumen+Zeigefinger ganz, Vesper Stoffmanschette über linkem Stumpf. Reviewer BESTANDEN ohne Block-A. Tschechow: Drei Stümpfe als Material-Folge, Marens Boot mit altem Namen (Maren-Tod-Echo), Vesper-Phantom-Stelle, Sub-Phase-Andeutung dezent. |
| 20 | ✅ erledigt | v2 | Vision 92% · Voice Alphina 95% | 2026-05-05 | Captivity-Folter, SLY-Primär. Velmar-Halsband-Mechanik korrekt nach `10-magie-system.md:80-99` (reaktive Absorption, matt-violett von innen, Moos/Gras-Niveau). Reviewer BESTANDEN ohne Block-A. Dom-Antagonist Varen ohne Heat. Tschechow: Stahlring-Glüh-Anzeige, Riss + Moos, Varen-Purpurstein-Ring, Geruchlosigkeit, Mar-Keth-Reveal-Setup. |
| 31 | ✅ erledigt | v2 | Vision 85% · Voice Alphina 88% | 2026-05-05 | Voice-Anchored Refit-Pipeline. Varen-Reveal-Dialog (B3-K37-Vorlauf), Heat: Drohung. JM-Primär (Macht-Asymmetrie, Reveal-Dehnung) + RY-Sekundär (körperliche Selbstbeobachtung). Vier Canon-Sätze sauber gesetzt (»Kleine naive Alphina.«, *Du warst sauberer zu lesen als Sorel.*, *Sie starb in der Küche.*, *Ich habe dich nie angesehen. Nur deinen Frequenzwert.*). Heat-Echo Varen Modus C dezent (Dornenranke mit Purpurblüte am Türrahmen) parallel zu grünem Trieb als Halt-Markierung an Thalassien. Tschechow: Wirbelsäulen-Narbe (B1-K38-Echo), Halt-Berührung-Faser am Handrücken, Frequenzwert-Setup (B3-Akt-IV-Reveal), Setzkasten-Bild (Druckerei/Velmar-Prüfer-Echo). Antislop BESTANDEN (»wie«-Vergleiche 6→2, »Das war« 3 borderline mit Funktion, Sein-Cluster 17/1052W). Du/Sie-Asymmetrie konsequent (Varen duzt, Alphina siezt). |
| 25 | ✅ erledigt | v2.1 | Vision 92% · Voice Vesper 95% | 2026-05-05 | Vesper/Nyr Thar-Register, leise BDSM. Setting-Verlegung B1-Vael → B2 Akt III Thar-Kem-Werkstatt (canon-konform). Schachturm-Tasten-Anker (kalt → warm). Mini-Fix: Beat → Takt (Anglizismus). Tschechow: Druckspuren-Mechanik, Knopf in Ölwanne, Schraubenzieher-Lineal. Asymmetrische Power-Dynamik via Dock-Geometrie. |
| 26 | ✅ erledigt | v2.1 | Vision 84% · Voice Alphina 90% | 2026-05-05 | Alphina/Varen Machtpakt, Heat Drohung. JM+Réage+SLY. Reviewer Block-A-Fixes: Adverb-Tag „nüchtern" raus, „Welt-Marker"-Doppelglosse raus, Telling-Schluss verkürzt, Stakkato-Triade aufgelöst, blieb 10→6 / ließ 8→5. Heat-Echo Varen kanonisch (Dornenranke + Purpurblüte mit zweiter Knospe-Eskalation). Tschechow: Riss-im-Pakt-Subtext, schwarze Wurzeln in Diele. |
| 27 | ✅ erledigt | v2.1 | Vision 90% · Voice Alphina 92% | 2026-05-05 | Alphina-Sub/Vesper-Dom B3-K40, explizit BDSM. Réage+Rampling+SLY. Hand-Geometrie kanonisch (Daumen+Zeigefinger ganz, drei Stümpfe), Vesper-Stoffmanschette, Vesper-Einarmig-Bondage übers Kreuz. Reviewer Block-A-Fixes: Schritt-Doppel, Puls→Handgelenk, Maren-Vergleich raus, Krug-Doppel aufgelöst, Anaphern-Quartett gebrochen. Sub durch Scham nach Varen-Zeit. Anti-Flora-Negativ (Salzkraut-Topf — keine Wedel) als Heilungs-Beleg. |
| 28 | ✅ erledigt | v3.1 | Vision 78% · Voice Alphina 82% | 2026-05-05 | Sorel-Tod-Moment, Heat Trauer. v3: Stein-Bruch-Mechanik korrigiert (Pflanzen wachsen DURCH organisches Geflecht im Moragh-Boden, brechen Stein als Konsequenz an Spaltkanten). v3.1: Block-A-Fixes (Selbsterkenntnis-Glanz, Doppel „notierte", Henrik-Aphorismus-Doppel, „Etwas Spitzes" → Wurzel, „wie geronnener Saft" raus). Trauer-Manifestation schwarze Triebe + Blüten purpur/blut-rot, Wirbelsäulen-Wurzel als Körper-Konsequenz. |
| 29 | ✅ erledigt | v2 | Vision 92% · Voice Alphina 94% | 2026-05-05 | Portal-Öffnung Ritual, Heat Drohung. Reviewer ANGENOMMEN ohne Block-A. Vier Resonanzen mit eigenen Mikro-Choreografien (N/O/W/S), Steinkreis-Canon (7 Purpursteine, vier besetzt + drei leer als Sitz der Kraft). „Kein Wort dafür. Ein Bild." als Magie-via-Vorstellung-Beat. Areligiös (kein Liturg-Ton). Tschechow: Druckerei-Geruch (Runa), Wedel-Tschechow für Alphina, Welt-Schock-Sinnes-Trias. |
| 30 | ✅ erledigt | v2 | Vision 94% · Voice Maren 92% | 2026-05-05 | Verwüster Vael/Marens Tod, Maren-POV. SLY+JM. Reviewer ABNAHME mit drei Mikro-Fixes (Denk-Tag Z.65, Doppel-Negation Z.71, Z.41 zwei Negationen). Schemen-Mechanik perfekt (lautlos durch Wand, Frost-Klinge nur bei aktiver Magie). Tschechow-Architektur: Eichenkeule, Macke im Türrahmen, Notizbuch „Expedition 2", K30-Tunnel-Frost-Echo, „Ich habe sie hergeschickt" als Schluss-Hammer. |
| 31 | ✅ erledigt | v2.1 | Vision 88% · Voice Alphina 90% | 2026-05-05 | Varen-Reveal-Dialog, Heat Drohung. v2.1: Block-A-Fixes (Meta-Zählung weg, Stakkato positiv, Doppel-Negation gestrichen, Adjektiv-Anhängsel weg). Vier Canon-Sätze sauber gesetzt (»Kleine naive Alphina.«, *Du warst sauberer zu lesen als Sorel.*, *Sie starb in der Küche.*, *Ich habe dich nie angesehen. Nur deinen Frequenzwert.*). Heat-Echo Modus C dezent. Tschechow: Wirbelsäulen-Narbe K38, Faser am Handrücken. Du/Sie-Asymmetrie konsequent. |
| 32 | ✅ erledigt | v2 | Vision 92% · Voice Alphina 90% | 2026-05-05 | Schemen-Angriff, Heat Gewalt. SLY-Reinform. Reviewer SHIP (keine Fixes). Schemen-Lautlosigkeit konsequent (kein Schritt/Reibung/Atemzug, Daumenbreit über Steinen, Staub bleibt liegen). Schaden NUR durch aktive Magie (Eis-Welle aus Fingerspitzen, weißer Reif-Finger als Auslöser). Frost-im-Knochen-Tschechow K30 sauber gesetzt. Heilung BILD/QUELLE/FOLGE perfekt. |
| 33 | ✅ erledigt | v2 | Vision 92% · Voice Alphina 95% | 2026-05-05 | Talven-Blutmagie. POV-Wechsel Talven→Alphina (Tschechow-Setup für B3-K30 Fehlurteil — Alphinas Botaniker-Brille wird zum Selbsttäuschungs-Werkzeug). Reviewer STRONG ACCEPT. Talven-Mechanik kanonisch (Eschenholz-Messer + Tonschale + Kristall im Messinggestell, schmaler roter Streifen, parallele Narbenlinien, kalte Hände passive Veränderung). KEINE „Resonanz-Ernte". Selbst-Demaskierung via „Probe, die zu gut zur These passte". |
| 34 | ✅ erledigt | v2.2 | Vision 92% · Voice Alphina 94% | 2026-05-05 | Runa-Verzeihung, Heat Trauer. v2.2: Glutmoos-Manifestation (Heat-Echo Runa Modus C statt Knospe). Schluss-Beat Z.103-111: Glutmoos-Polster in Mauerritze neben Seitentür, fingernagelgroß, rötlich-glühend; Alphina erkennt zum ersten Mal magisch (Verzeihungs-Beat als Selbst-Erkenntnis); Runa hatte es täglich gespürt, nicht gefegt — Asymmetrie-Auflösung als Tat. Drei-Sätze-Echo, Canon-Dialog, schwarze Daumen-Spur K38 alle erhalten. Master-Update Glutmoos in 4 Files vollzogen. |
| 35 | ✅ erledigt | v2 | Vision 88% · Voice Alphina 90% | 2026-05-05 | Folter brutal. POV-Wechsel Nyr→Alphina, Setting B2 Bund-Captivity-Reverse (Drael Bund-Inquisitor). Frontmatter-Hinweis: „hypothetisches Setup / B3-Spekulation, B2-Canon: Varen, nicht Drael". Velmar-Halsband-Mechanik korrekt. Drei-Fragen-Pause-Rhythmus als Folter-Skelett. Halsband-Sperre liest Trieb als Pflanze, nicht als Wirken (Canon-Extrapolation). Distanzierung als Trauma-Marker (SenLinYu-Niveau). |

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
