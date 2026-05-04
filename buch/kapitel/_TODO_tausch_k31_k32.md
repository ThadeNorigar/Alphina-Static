# TODO — Tausch K31 ↔ K32 nach Final

**Stand 2026-05-03.** Beschluss im /ausarbeitung-Pre-Check für B1-K31.

## Hintergrund

Chronologische Reihenfolge:
- **K30** Sorel · 8. Nebelmond Nacht → 9. Nebelmond Morgendämmerung · Hafengasse-Nacht-Angriff
- **JETZT K32** Runa · 9. Nebelmond Tag/Abend · Druckerei allein, Verarbeitung K30, Selbst-Erkenntnis, Setup K34
- **JETZT K31** Alphina · 14. Nebelmond Tag · Marktplatz-Schemen-Mord, Runas Hände öffentlich, *„Heute Abend. Bei dir."*
- **K33** Vesper · später · Schwerkraftanomalie

In der Buch-Lesereihenfolge ist die Sequenz **K30 → JETZT-K32 → JETZT-K31 → K33** — die Kapitel-Nummern stehen also gegen die Chronologie.

## Aktueller Stand (während Ausarbeitung)

Wir arbeiten parallel an beiden Kapiteln mit den **alten Nummern** (K31 = Alphina, K32 = Runa). Die zeitleiste.json + Handoffs tragen die korrekten Datums-Anker (K32 = 9. Nebelmond, K31 = 14. Nebelmond), aber die Kapitel-Nummern bleiben ungetauscht, bis beide final sind.

## Tausch-Aktion (nach beidseitigem Final)

Wenn K31 + K32 beide den Status `final` haben, wird folgende Renumberung durchgeführt:

1. **Datei-Umbenennung:**
   - `B1-K32-runa.md` → `B1-K31-runa.md` (oder neuer Name)
   - `B1-K31-alphina.md` → `B1-K32-alphina.md`
   - Dazu `*-entwurf.md` und ggf. `*-handoff.md` (falls noch vorhanden) konsistent.

2. **zeitleiste.json:**
   - Kapitel-Nummer-Felder (`"kapitel": "32"` / `"kapitel": "31"`) tauschen.
   - tz_sort bleibt logisch korrekt (K-neu-31 = 551.605, K-neu-32 = 551.62).

3. **buch/status.json:**
   - Eintrag-Tausch K31 ↔ K32.

4. **buch/kapitel-summaries.md:**
   - Einträge umnummerieren.

5. **Cross-Referenzen prüfen + ändern:**
   - `buch/pov/sorel-schreibblatt.md` (referenziert K-Nummern)
   - `buch/pov/maren-schreibblatt.md`
   - `buch/pov/alphina-schreibblatt.md`
   - `buch/pov/runa-schreibblatt.md`
   - `buch/pov/vesper-schreibblatt.md`
   - Memory-Files (alle ⚡-Memories prüfen, die K31/K32 referenzieren)
   - K33+, K34+ Entwürfe/Handoffs (falls referenzieren)
   - `buch/_archiv/` falls historisch (Aktpläne)
   - `buch/zeitleiste-html-templates/` falls vorhanden

6. **Aktplan + Storyline:**
   - `buch/00-storyline.md` (falls Kapitel-Nummern-Listen)
   - Akt-Pläne im Archiv (falls relevant für K31-K32-Strecke)

7. **Stil-Skills + Doku:**
   - `.claude/commands/*.md` (falls feste K-Referenzen)
   - `CLAUDE.md` (falls Beispiele)

8. **Git-Commit-Format:**
   - Vorbild: `feat(B1-K31): Final — Runa, ...W` (alter Inhalt von K32 unter neuer Nummer)
   - Sammel-Commit `chore(B1): Tausch K31↔K32 (Lesereihenfolge sauber)`

## Vorab-Vermerke (während K31/K32 ausgearbeitet werden)

- **K32-Entwurf-Inhalt-Refactor** ist eigene Aufgabe (siehe Task #13): Cross-POV-Anker auf K30 statt K31, Probebrett-Brandfleck entfällt, Datum 9. Nebelmond. **Vor dem K32-Final** durchführen.
- **K31-Entwurf** bleibt mit „sechs Tage nach K30" konsistent — kein Beat-Refactor nötig.
- **K30-wip-Schluss** sollte berücksichtigen: Runa geht später am Tag (oder am Folgetag) zur Druckerei, weil sie allein sein will. Das ist Cross-Anker zu (jetzt) K32. Bei K30-Phase-4-Stil-Check prüfen.

## Risiken bei verzögertem Tausch

- Solange Tausch nicht durchgeführt: Lesereihenfolge K30 → K32 → K31 → K33 bleibt verwirrend für jede Person, die nach Kapitel-Nummer liest.
- Cross-POV-Notizen referenzieren weiterhin alte Nummern — Tausch macht alle Referenzen ungültig, daher zentral durchführen.
- Memory-Eintrag `project_b2_k01-k27_canon.md` referenziert K31-K33 — prüfen, ob die Reihenfolge dort zur Buch-Lesereihenfolge oder zur Chronologie spricht.
