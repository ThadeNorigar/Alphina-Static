# Charakter-Files — Konsistenz-Audit

**Status:** in Arbeit
**Gestartet:** 2026-05-02
**Ziel:** Alle Charakter-Files prüfen, dass jede Information im richtigen File steht und Plot-Anker sauber gegen Synopsen + Zeitleiste verankert sind.

---

## Methode

**Phase 1 — Cross-Character-Drift (Inhalt im falschen File?)**
Pro Charakter-File prüfen, ob Inhalte über *andere* Charaktere drin sind, die in deren Dossier gehören. Single Source of Truth herstellen.

**Phase 2 — Plot-Anker pro Charakter**
Pro Charakter alle Plot-Ideen aus dem Dossier extrahieren, gegen `synopse-b2.md`, `synopse-b3.md`, `zeitleiste.json` matchen. Konflikte klären, Lücken füllen.

**Phase 3 — Zeitleisten-Konsolidierung**
Pro Hauptfigur sicherstellen, dass jedes Schlüssel-Erlebnis als Zeitleisten-Event verankert ist (oder bewusst als Aktplan-Detail belassen).

---

## Phase 1 — Cross-Character-Drift (Status pro File)

### Master-Files

| File | Geprüft | Findings | Aktion |
|---|---|---|---|
| `19-varen.md` | ✓ 2026-05-02 | §8 Sorel-Tod-Szene, §9 Alphina-B2-Bogen, §10 Alphina-B3-Bruch, §11 Alphina-Farblogik — gehört nicht ins Varen-File | Befund 1.1 |
| `11-nyr.md` | ✓ 2026-05-02 | „Buch 2 Ende — Der Verrat" + „Buch 3 — Schlüsselszene" beschreiben Vesper-Bogen, nicht Nyr; „Runa als Verfolgerin" beschreibt Runa-B3 | Befund 1.2 |
| `13-talven.md` | ✓ 2026-05-02 | sauber | Befund 1.3 |

### POV-Dossiers

| File | Geprüft | Findings | Aktion |
|---|---|---|---|
| `pov/alphina.md` | ✓ 2026-05-02 | sauber | — |
| `pov/sorel.md` | ✓ 2026-05-02 | sauber | — |
| `pov/vesper.md` | ✓ 2026-05-02 | sauber | — |
| `pov/maren.md` | ✓ 2026-05-02 | klein: ein Satz Varen-Aktion in Tod-Sektion (gerechtfertigt) | belassen |
| `pov/runa.md` | ✓ 2026-05-02 | sauber | — |
| `pov/elke.md` | ✓ 2026-05-02 | **massiv:** Tod-Sektion enthält B3-Plot von Maren/Varen/Alphina/Talven | Befund 1.4 |
| `pov/iven.md` | ✓ 2026-05-02 | sauber (aber Daten-Konflikt D3) | — |
| `pov/drael.md` | ✓ 2026-05-02 | sauber | — |
| `pov/tyra-halvard.md` | ✓ 2026-05-02 | sauber (Daten-Konflikt D10) | — |
| `pov/syra-halvard.md` | ✓ 2026-05-02 | sauber (Daten-Konflikte D4+D9) | — |
| `pov/kelvar-velkan.md` | ✓ 2026-05-02 | sauber | — |

### Nebenfiguren

| File | Geprüft | Findings | Aktion |
|---|---|---|---|
| `nebenfiguren/*` (23 Files) | grob (Agent-Lauf) | TZ-154-Resonanzen-Konflikt (Lene Wasser vs. Holz, Kesper Licht vs. Luft); Henrik Gärtner vs. Torwächter; Lene-Dahl 2047 vs. 2037 | siehe Audit 1. + 2. Lauf, separate Findings |

---

## Befunde Phase 1

### Befund 1.1 — `19-varen.md` enthält Alphina + Sorel-Inhalt

**Quelle:** `19-varen.md` ist am 2026-04-09 als „Session Grundplot" angelegt — Konsolidierungs-Session mit vier Themen in einer Datei. Mai-Updates flossen nur in `synopse-b2/b3` und `pov/alphina.md`, nicht zurück in das Varen-File. Drift-Erzeuger Nr. 1.

**Was gehört woanders:**

| Sektion | Inhalt | Master sollte sein | Status |
|---|---|---|---|
| §8 „Sorel-Todesszene K37+K38+K39" | Drehbuch-artige Beschreibung von B1-K28/K29/K30 (alte Numerierung K37–K39) | `pov/sorel.md` Tod-Sektion **oder** Aktplan-Eintrag B1-Akt-Schluss | umziehen, Numerierung aktualisieren |
| §9 „Alphinas Buch-2-Bogen (neu strukturiert)" | Akt I bis Endakt mit Bund-Training, Quellen-Zerstörung, Captivity, Sex mit Varen | `synopse-b2.md` (heute Master) | Inhalt ist veraltet (Schweige-Verrat statt Hybrid-Geständnis) — **gute Detail-Beats retten**, dann Sektion löschen |
| §10 „Buch 3 — Der Bruch durch Schweigen" | Hybrid-Geständnis-Strategie, „Verrat ist das Schweigen", stiller Tod Varen | `synopse-b3.md` | Inhalt veraltet — **Detail-Beats retten** (z.B. „Jeder Kuss eine Lüge durch Auslassung"), dann Sektion löschen |
| §11 „Farblogik von Alphinas Resonanz — ausführlich" | Wann grün, wann schwarz/rot, physiologische Erklärung | `pov/alphina.md` Sektion „Zorn-Farbpalette" — **bereits dupliziert** | redundant, löschen |

**§8 Sorel-Todesszene — Cleanup-Status (2026-05-02):**

- ✓ **GERETTET:** 8.8 Bindungs-Berührung-Choreographie → `pov/alphina.md` Tschechow
- ✓ **GERETTET:** 8.12 Licht-Resonanz schwächer gegen Zeit-Bindung → `pov/sorel.md` Tschechow
- ✓ **GERETTET:** 8.17 Lichtsäule aus Sorels Leben (Sterbe-Mechanik) → `pov/sorel.md` Tschechow
- ✓ **GERETTET:** 8.19 Kamera stirbt mit Sorel → `pov/sorel.md` Tschechow
- ✓ **GERETTET:** 8.25 Wirbelsäulen-Narbe lebenslang → `pov/alphina.md` Tschechow
- ✓ **GERETTET:** 8.27 Drei-Wunden-Set → `pov/maren.md`, `pov/vesper.md`, `pov/runa.md`
- ✓ **GERETTET:** 8.30 Magie-Mechanik azyklisch (Wut speist) → `pov/alphina.md` Tschechow
- ✓ **GERETTET:** 8.32 Sorel-Blüten bleiben für immer → `pov/sorel.md` Tschechow (Alphina-Echo war schon in Zorn-Farbpalette)
- ✗ **VERWORFEN:** 8.26 Größerwerden um halben Meter (body-horror, Autor-Entscheidung 2026-05-02)
- ✓ **GERETTET (a/b/c) + STREICHEN d:** 8.6 Erscheinung — Erstwahrnehmung-Tschechow nach `pov/alphina.md`, Rest redundant zu §1
- ✓ **GERETTET + KORRIGIERT:** 8.16 Bindungsmagie — wurde in §1b Binden-Stufe-6 ergänzt um den Hinweis „Bindungsmagie wirkt nur auf Schemen, nicht auf Thalassier oder Moragh-Geborene". Reaktions-Lag wurde aus dem Binden-Eintrag rausgenommen und als allgemeine Halt-Magie-Notiz neu verortet (Druck/Zeit/Energie umlenken).
- ✓ **GERETTET + KORRIGIERT:** 8.28 — Magie-Mechanik + taktisches Profil als Block in `19-varen.md` §1b. **Korrektur:** kein „Blut spucken", kein „Anfänger-zermalmen", kein Backlash. Stattdessen: taktischer Rückzug, Bannen-Mechanik, Reservoir-Risiko gegen azyklisch-emotional-verstärkte Thalassier-Magie. Verweis auf `10-magie-system.md` (neuer Block dort).
- ✓ **GERETTET:** 8.29 Abgangstext — *„Euer Freund trat zwischen mich und sie; mein Schutz hat geantwortet. Was danach in ihm zerbrochen ist, kam aus ihm. Sein Licht war größer als sein Maß. Bedenkt das, ehe ihr mich zum Grund erklärt."* — eingebaut in §1 (Stimm-Beispiel), §1b (Mechanik-Block), §13 (Entscheidungs-Tabelle). Alte Floskel „Wir sehen uns nicht das letzte Mal" überschrieben.
- ✓ **HALT-MAGIE-CANON präzisiert:** Bindungsmagie wirkt nur auf Schemen. Auf Thalassier und Moragh-Geborene wirkt eine Kombination Druck (festhalten) + Zeit (verlangsamen) + Energie (Resonanz dämpfen). Aktive Resonanz-Träger können die Energie-Komponente lokal kompensieren. In `pov/alphina.md` 8.8 + `pov/sorel.md` 8.12 + `pov/sorel.md` 8.17 + `19-varen.md` §1b angepasst.
- ✓ **CANON-UPDATE in `10-magie-system.md`:** (a) Z.646 Korrektur 2–3 Stunden → 1–2 Tage; (b) neuer Block „Reservoir und Befehlstreue" + „Bindung beenden — Bannen vs. Lösen" + „Aggressions-Tendenz nach Auflösung" mit Bewertungs-Skala (Lesart C, reaktiver Schutz-Befehl = −1) und Konsequenz-Beispielen B1-K38 / B3 Akt II / B3 Akt IV.
- ✓ **KAPITEL-KORREKTUR:** alle B1-K28/K29/K30-Verweise in den geretteten Beats (Alphina/Sorel/Maren/Vesper/Runa-Dossiers + 19-varen.md §1b) auf B1-K38 umgemappt — Kampf passiert auf Moragh-Seite (B1-K38 = „Moragh-Ankunft + Varen + Sorel stirbt + Alphinas Explosion + Beruhigung" laut Zeitleiste).

**§8 Sorel-Todesszene — Status: ✓ vollständig bearbeitet.** Bereit zum Löschen aus `19-varen.md`, sobald §9–§10 ebenfalls bearbeitet sind.

---

### §11 Cleanup — Status: ✓ erledigt 2026-05-03

**Drei Beats nach `pov/alphina.md` Zorn-Farbpalette gerettet:**
- „Andere drei sehen es und verstehen: Alphina gehört hierher" (Cross-POV-Horror-Pointe)
- „Grün als Erinnerungs-Echo" (wenn sie an Thalassien denkt)
- „Tschechow-Barometer-Funktion" (Leserin liest die Farbe seit B1-K38)
- Implizit-Beispiel „Rinde wie Kohle im Regen" ergänzt

**Sektion §11 in `19-varen.md` reduziert auf einen Verweis-Stub:** Master ist `pov/alphina.md`.

**§9 + §10 + §11 Status:** ausstehend nach §8-Cleanup.

**Empfehlung:** Wenn §8 abgeschlossen ist, §9 (Alphina-B2-Bogen alt) und §10 (B3-Bruch alt) sichten — viel davon ist in `synopse-b2/b3` schon Master, also primär STREICHEN nach Detail-Rettung. §11 Farblogik komplett redundant zu `pov/alphina.md` Zorn-Farbpalette → STREICHEN.

**Restliche Detail-Beats aus §9/§10/§11, die noch retten-würdig sind (Vorausschau):**

- §9: Schlaf-Haine im Bund (Wald wächst um ihr Bett, Bund-Meister beeindruckt+beunruhigt)
- §9: Sorel als schwarzer Baum mit blutroten Blüten in der Mitte des Hains (B2-Tschechow)
- §9: „Verunreinigung"-Vokabular der Bund-Meister
- §9: Mar-Keth/Dulrath-Ost/Reshkol-Captivity-Tour mit Skeletten + Mauer mit Namen + Kind-jetzt-Greis
- §9: Schmied-Kollaps bei Quellenzerstörung („Werkzeuge brauchen Magie")
- §10: „Jeder Kuss eine Lüge durch Auslassung" (Tonfall-Anker, falls Schweige-Bruch in irgendeiner Form bleibt)

---

### Befund 1.2 — `11-nyr.md` enthält Vesper- + Runa-Inhalt + alten Plot

**Quelle:** Im April-Stand. Mai-Updates (Vesper geht freiwillig zur Thar als Stratege; Runa bleibt beim Bund) sind in `synopse-b2/b3`, `pov/vesper.md`, `pov/runa.md` aktualisiert, aber nicht in Nyr.

**Was gehört woanders:**

| Sektion | Inhalt | Master | Status |
|---|---|---|---|
| „Buch 2, Akt II — Vesper geht mit" | Vesper bei Thar, Erstbegegnung mit Nyr in Werkstatt, BDSM-Auftakt | `pov/vesper.md` + `synopse-b2` | Vesper-Anteil umziehen; Nyr-eigener Anteil bleibt |
| „Buch 2, Ende — Der Verrat" | Vesper gibt Position der anderen an Thar — VERALTETER PLOT (kein Verrat in synopse-b2/b3) | nirgendwo (überholt) | **streichen** oder als alte-Variante archivieren |
| „Buch 3 — Schlüsselszene: Nyr wechselt die Seite" | Vesper rechnet, Nyr legt Bauplan vor, „Fünfzehn Sekunden" | bleibt teilweise im Nyr-File (Nyrs Wende-Moment) — Vesper-Anteil als Spiegel in `pov/vesper.md` referenzieren | Nyr-zentriert behalten, Vesper-Sicht in Vesper-Dossier ergänzen |
| „Buch 3, Rückkehr" — Maren schlägt Vesper ins Gesicht | Maren-Reaktion auf Vesper — Maren-/Vesper-Plot, nicht Nyr | überholt? klären — passt das zur neuen Linie (Vesper geht zu Alphina, Nyr zu Runa)? | **KLÄREN** |
| „Runa — die Verfolgerin" | Runa beim Konglomerat aufgestiegen, jagt Nyr+Vesper | überholter Plot (Runa bleibt beim Bund) | **streichen** |

**Detail-Beats aus Nyr-File, die zu retten sind:**

- Kessler als Bestien-Persönlichkeit (40 Tonnen, Bulle/Stier-Form, Reservoir-Kern Brustkorb 6–8 h, Nyr nennt sie beim Namen) — bleibt im Nyr-File ✓
- Druck-Resonanz-Mechanik (Luft pressen, Metall biegen, Knochen brechen ohne Berührung) — bleibt ✓
- BDSM-Dynamik Nyr+Vesper (Nyr presst ihn an Metallwand, Luft wird dünn, blaue Flecken aus Luft, Druckstellen ohne Finger) — Beziehungs-Anteil teilen zwischen `11-nyr.md` und `pov/vesper.md`
- Autonome-Bestien-Alptraum (B3 Trigger-Bild für Nyrs Wende) — bleibt ✓
- „Werkzeug"-Kipppunkt — bleibt ✓ (Nyr-Kern)

**Empfehlung:** Nyr-File auf Nyrs eigenen Bogen reduzieren. Vesper-Verrats-Sektion + Runa-Verfolgerin-Sektion sind überholt — entweder streichen oder ins `_archiv` verschieben.

---

### Befund 1.3 — `13-talven.md`

**Geprüft 2026-05-02. Sauber.** Erwähnungen anderer Figuren sind alle aus Talvens Sicht (sein Hunger auf Alphinas mühelose Magie, Beziehung zu Elke als Kontakt, Abgrenzung Talvens Blutmagie zu Varens Resonanz-Ernte). Kein Plot-Beat über andere Charaktere, der woanders gehören müsste.

---

### Befund 1.4 — `pov/elke.md` Tod-Sektion enthält B3-Plot

**Geprüft 2026-05-02. Cross-Char-Drift.**

Die Sektion „Tod in Buch 3 — Akt II" (Z. ~111–125) erzählt nicht nur Elkes Tod, sondern halben B3-Akt-II/III/IV-Plot:

| Inhalt der Sektion | Wessen Plot ist das? | Master sollte sein |
|---|---|---|
| „Kurz vor ihrem Tod übergibt **Maren** ... Elke ein Velmar-Dokument" | Marens Aktion (Bündel-Übergabe) — **außerdem Richtung falsch** (Memory-Synopse: Elke → Maren, nicht Maren → Elke) + Kapitel falsch (K41 statt K39) | `synopse-b2` K16 (führender Master) — Elke-File sollte nur referenzieren |
| „Varen findet heraus, dass Elke das Dokument hat ... Schemen tötet sie in der Küche" | Varens Aktion (Mord-Auftrag) | `synopse-b3` Akt II + `19-varen.md` (Varens Plot in B3) |
| „Alphina verdächtigt Talven zu Unrecht — drei gefälschte Beweise" | Alphinas Verdachts-Linie, Varens Falle | `synopse-b3` Akt II + `pov/alphina.md` |
| „Alphina tötet Talven in Akt III" | Alphina-/Talven-Plot | `synopse-b3` Akt III + `13-talven.md` (Tod-Eintrag) |
| „Erkennt erst in Akt IV (durch Varens Küchen-Satz), dass Varen Elke getötet hat" | Alphinas Akt-IV-Reveal | `synopse-b3` Akt IV + `pov/alphina.md` |

**Was bleiben sollte in `pov/elke.md`:**
- Elkes letzter Akt: Bündel an Maren übergeben (richtige Richtung), mündlicher Hinweis „Unter dem Stein, wo nichts wächst"
- Elkes Tod-Tatort + Anomalien (Würgespuren, Tau-Spuren-Fehlen, Basalt-Splitter weg, Küche sauber gewischt)
- Elkes Grab bei Dravek, Alphina besucht es nach Akt-IV-Enthüllung

**Was umziehen oder entfernen:**
- Detail-Plot „Schemen-Auftrag, Tatort-Inszenierung im Garten" — gehört in `synopse-b3` Akt II als Varen-Beat (Master); Elke-File verweist
- Talven-Verdachtskette + Talvens Tod — gehört in `synopse-b3` + `13-talven.md`; Elke-File verweist
- Akt-IV-Reveal-Linie — gehört in `pov/alphina.md` Akt-IV-Sektion + `synopse-b3` Akt IV

---

### Befund 1.5 — Andere POV-Dossiers (alphina, sorel, vesper, maren, runa, iven, drael, tyra, syra, kelvar)

**Geprüft 2026-05-02. Im Wesentlichen sauber.**

Alle Dossiers haben standardisierte Sektionen (Berufslinse, Körper-Leitmotiv, Wissensstand, Tschechow-Waffen, Beziehungs-Dynamik). Beschreibungen anderer Figuren erfolgen aus der Sicht der POV-Figur (z.B. „Sorel hat Grenzen" in alphina.md ist Alphinas Wahrnehmung) — das ist legitim.

**Kleinere Berührungen mit Cross-Char-Drift, aber unter der Schwelle:**

- `pov/maren.md` Tod-Sektion (B3-I8): erwähnt „Varen manipulierte Orath-Rufer zur Vergeltungs-Beschwörung" — beschreibt Varens Aktion. Ein Satz, gerechtfertigt als Erklärung warum Maren stirbt. **Belassen mit Verweis** auf `synopse-b3` Akt II.
- `pov/vesper.md` Buch-3-Sektion: „Alphina-Rettung statt Nyr" + „Paar-Ende mit Alphina K80" — beschreibt Vespers Bewegungs-Linie, kein fremder Plot. ✓
- `pov/iven.md` Tat-Linie: enthält Daten-Konflikt mit Synopse (Akt II vs. Akt IV — siehe Drift D3), aber kein Cross-Char-Drift.

**Bestätigt clean:** `alphina.md`, `sorel.md`, `vesper.md`, `runa.md`, `iven.md`, `drael.md`, `tyra-halvard.md`, `syra-halvard.md`, `kelvar-velkan.md`.

---

## Phase 1 — Schon gefundene Cross-File-Drifts (Vorlauf-Audit, andere Richtung)

Diese Drifts wurden bereits im 1./2. Audit-Lauf gefunden und betreffen Cross-File-Konsistenz, sind aber nicht „Inhalt im falschen File" — eher Datenpunkt-Inkonsistenzen:

| # | Aspekt | Datei A | Datei B | Status |
|---|---|---|---|---|
| D1 | Maren-Wasserweg-Kapitel | synopse-b2 + zeitleiste = K39 | `pov/maren.md` + `pov/elke.md` = K41 | offen |
| D2 | Bündel-Übergaberichtung Elke ↔ Maren | synopse-b2 K16: Elke → Maren | `pov/elke.md`: Maren → Elke | offen |
| D3 | Iven-Einführung | synopse-b3 = Akt IV | `pov/iven.md` = Akt II (I10) | offen |
| D4 | Marens Todesjahr | synopse-b3 + maren.md + zeitleiste sync = 2037 TZ | `syra-halvard.md` + `lene-dahl.md` = 2047 TZ | offen |
| D5 | TZ-154-Resonanzen | Memory `project_tz154_canon.md` (Lene=Holz, Kesper=Luft, Keldan=Eisen) | `lene-dahl.md` (Wasser), `kesper-holm.md` (Licht) | offen |
| D6 | Lene-Dahl-Gründungsjahr | `pov/maren.md` = TZ 151 | `lene-dahl.md` = TZ 154 | offen |
| D7 | Halvard-Familie in TZ 154? | `tohl.md`: „Doktor Halvard" 154 | Halvard-Linie ist nach Maren (1987 TZ+) | KLÄREN |
| D8 | Henrik-Funktion | `nebenfiguren/henrik.md` = Gärtner | `pov/sorel.md` = Torwächter | offen |
| D9 | Syra Übernahme-Jahr / I9-Datierung | synopse-b3: I9 = Syra mit 15 + Kelvar mit 25 (~2090 TZ) | `syra-halvard.md`: 2080 TZ Syra übernimmt Leitung | offen — Syra-Tat-Linie umrechnen |
| D10 | Tyra-Verwandtschafts-Generation | `tyra-halvard.md` = „Marens Ur-Großtante" | `pov/maren.md` = Tyra ist Marens Ur-Großnichte (richtig: jüngere Generation) | offen |
| D11 | `19-varen.md` Tippfehler MZ-/TZ-Berechnung | §6/§7: „MZ -0.42 = TZ 354" sollte ~TZ 386 sein | — | klein, später |

---

## Phase 2 — Plot-Anker pro Charakter (kommt nach Phase 1)

Wird gefüllt, sobald Phase 1 abgeschlossen ist. Dann pro Hauptfigur:
- Plot-Anker aus dem Dossier extrahieren
- Gegen Synopsen + Zeitleiste matchen (Status: Z+/A+/S+/KLÄREN/VERWERFEN)
- Konflikte klären, Lücken füllen

Reihenfolge geplant:
1. Alphina (Pilot bereits im Audit-Verlauf erstellt — siehe Konversation)
2. Sorel
3. Vesper
4. Maren
5. Runa
6. Varen
7. Talven
8. Nyr
9. Elke
10. Tyra Halvard
11. Syra Halvard
12. Kelvar Velkan
13. Iven
14. Drael

---

## Phase 3 — Zeitleisten-Konsolidierung (kommt nach Phase 2)

Pro Hauptfigur:
- Liste aller Schlüssel-Events aus dem Dossier
- Ist als zeitleiste.json-Event verankert? (oder bewusst Aktplan-only?)
- Lücken schließen

Außerdem: **Strukturproblem `tz`-Feld** in `zeitleiste.json` für B2/B3 ist sequenzieller Sortierschlüssel statt echtes TZ-Jahr (siehe Audit Lauf 1, Punkt 3.1) — entweder durchrechnen oder Feld umbenennen.
