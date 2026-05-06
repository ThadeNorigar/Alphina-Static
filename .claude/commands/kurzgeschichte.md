# /kurzgeschichte — Zufalls-Würfel-Kurzgeschichte aus dem Buch-Universum

Würfelt zufällige Figuren-Kombination, Setting, Begegnungsanlass und drei Akt-Sets aus dem Anatomie-Register und schreibt daraus eine ~1000-Wörter-Kurzgeschichte mit drei Sektionen (Setting / Begegnung / Akt).

**Modell:** Opus (Hauptsession). Kein Subagent — Stil-Druck verlangt direkten Kontrollblick.

**Output:** `buch/kurzgeschichten/{YYYYMMDD}-{slug}.md`

**Canon-Status:** Stil-Übung. KEIN Plot-Canon. Ändert weder `zeitleiste.json` noch `status.json`, kaskadiert keine Aktpläne. Bei Plot-Konflikten (Sorel ist tot in Moragh post-K46 etc.) Setting verschieben oder neu würfeln.

## Input

`$ARGUMENTS` = optionale Vorgaben (frei kombinierbar):

| Token | Wirkung |
|---|---|
| `kurz` | 500 statt 1000 Wörter |
| `lang` | 1500 statt 1000 Wörter |
| `heat` | erzwingt Heat-Level explizit (Alphina/Sorel-Register) |
| `bdsm` | erzwingt BDSM-Schwerpunkt (Vesper/Maren oder Varen-Captivity) |
| `tantra` | erzwingt Slow-Sex / Tantra-Schwerpunkt |
| `solo` | nur eine Figur, Solo-Akt |
| `figurnamen` | kommagetrennt, schränkt Pool ein (z.B. `vesper,maren`) |
| `welt:thalassien` / `welt:moragh` | Welt-Vorgabe |

Ohne Argument: voll zufällig.

## Phase 1 — Würfeln

### 1.1 Figuren-Pool ziehen

**Hauptfiguren** (häufigste Picks):
- **Alphina Farn** *(weiblich)* — Velde, Pflanzen-/Zellwachstums-Resonanz, dominant-emotional, kein BDSM-Register, Heat-Echo manifestiert sich als Pflanzen (Farne bei Sorel, Dornen mit Purpurblüten bei Varen, Glutmoos bei Runa)
- **Sorel** *(männlich)* — Nachtholm, Daguerreotypist, glatt rasiert, hat Grenzen, sub-emotional, kein Bart, kein BDSM-Sub-Register
- **Vesper Greve** *(männlich)* — Karst, Uhrmacher, Schach + Zeit-/Muster-Resonanz, Dom (mit Maren), Réage-Register, schwarzer Schachturm in der Tasche, grauer Gehrock + Weste + Leinenhemd, Daumen-Diagnose
- **Maren Ilves** *(weiblich)* — Grauküste/Vael, Werft-Erbin (Haron-Linie, NICHT Dahl), Wasser-Resonanz (Steuern/Kochen/Vereisen/Hören), Sub bei Vesper

**Nebenfiguren** (gelegentliche Picks):
- **Runa** *(weiblich)* — Journalistin, deckt auf, Nyrs Frau, eigenständig
- **Nyr** *(weiblich)* — eigenständig, lächelt, fordert Gerechtigkeit ein, Runas Frau
- **Varen** *(männlich)* — Velmar-Präparator (Antagonist B2), eloquent/argumentativ/wissbegierig, Mitte–Ende vierzig, extrem gutaussehend, violette Augen, stärkster Magie-Dämpfer
- **Tyra Halvard, Syra Halvard** *(weiblich)* — Halvaren-Linie, B2-Akteurinnen
- **Iven, Drael, Kelvar Velkan, Elke** — Geschlecht/Detail aus `buch/pov/<name>.md` (vor Pick lesen)

**Vor jedem Pick:** Geschlecht und Pronomen aus dem POV-Dossier abgleichen, bevor Akt-Set zugeordnet wird. FF-Bögen verlangen zwei Frauen, MF/MM/FFM/MMF entsprechend. Wenn unsicher: `buch/pov/<figur>.md` lesen, bevor gewürfelt wird.

**Ziehung:** 2 Figuren (60%), 3 Figuren (30%), 1 (Solo, 5%), 4+ (Multi-Player, 5%). Wenn `solo`-Token: 1 Figur. Wenn `figurnamen`-Vorgabe: Pool darauf einschränken.

**Plot-Constraints:**
- Sorel stirbt in B1-K46 — bei Moragh-Setting nur pre-K46 oder AU
- Alphina + Sorel: KEIN BDSM-Register. Sie führt, er hat Grenzen, aber das ist Charakter, nicht D/s-Spiel. Heat-Sets only (Cunni, Penetration, Cum-Akte, Schwellen-Stopp ohne Befehls-Grammatik)
- Vesper + Maren: BDSM voll erlaubt (Réage-Register), siehe `buch/pov/vesper-schreibblatt.md` + `buch/pov/maren-schreibblatt.md`
- Varen mit Sub-Figur: Velmar-Captivity-BDSM mit Magie-Dämpfung (Lederhalsband Stufe 5+, Stahlring matt-violett glühend) — siehe Memory `project_magie_daempfung_lederhalsband.md`
- Halvara-Kel-Geometrie B2: Tyra/Syra-Achsen, siehe `06-09-buch2-akt*.md`

Bei Konflikt: neu würfeln, max. drei Versuche, dann Vorgabe entspannen.

### 1.2 Welt + Ort + Tageszeit + Witterung

**Welt** (60% Thalassien, 40% Moragh, oder Vorgabe):

**Thalassien-Orte:**
- Vael — Hafen mit Werften, Marktstraße, Marens Werftbüro, Sorels Atelier, Alphinas Botanikgarten, Vespers Wohnung über der Uhrmacherei (NICHT mehr ab 12. Glutmond, siehe Memory), Privatzirkel-Salons, Stadtpalais
- Velde — Tidelände, Alphinas Familienanwesen mit Heilkräuter-Garten
- Nachtholm — Freistadt, Sorels Heimat, kühler Hafen
- Karst — Innenlande, Vespers Heimat, Schach-Stadt
- Grauküste — Marens Heimat, Werft-Tradition

**Moragh-Orte:**
- Stadt der Schemen — Hauptort, Velmar-Anwesen, Halvaren-Anwesen
- Karst-Hochland (Moragh) — purpurne Steine, Quellen-Stelle
- Dornwald — Pflanzen wachsen DURCH den Stein, Quellen-Bruch-Logik (Memory: `project_stein_quellen_pflanzen_resonanz.md`)
- Wasserweg — Marens Solo-Strecke (B2-K39)

**Tageszeit:** Morgendämmerung / Vormittag / Mittag / Nachmittag / Abend / Nacht / Spät-Nacht (Würfel)

**Witterung:**
- Thalassien: Erden-Wetter (Regen, Sturm, Sonne, Schnee, Nebel — saisonal nach Monat aus `00-welt.md` tz_kalender)
- Moragh: zwei Monde, Gezeiten-Logik, Memory `project_zwei_monde_moragh.md`. KEIN einmondig.

**Monatsname:** thalassischer Kanon (Eismond, Sturmmond, Saatmond, Grünmond, Blütenmond, Lichtmond, Glutmond, Erntemond, Herbstmond, Nebelmond, Frostmond, Dunkelmond). NIE realweltliche Monate.

### 1.3 Begegnungs-Anlass

Würfel-Pool:

| Anlass | Beispiel |
|---|---|
| Wiedersehen nach Trennung | Sie war zwei Wochen verreist; er kommt zurück, findet sie im Atelier |
| Gemeinsame Aufgabe | Recherche im Archiv, Bergung im Hafen, Brief-Übersetzung |
| Einladung zu Privatzirkel | Salon, Maskenball, Soiree mit anderen Paaren |
| Streit, der in Akt umkippt | Eifersucht, Plan-Differenz, Geheimnis aufgedeckt |
| Setup-Erfüllung | Sie hatten vereinbart: Tür angelehnt, Sub bereit, irgendwann zwischen X und Y |
| Brief-Aufforderung | „Komm um halb sieben. Wie immer." |
| Schicksal | Sturm, eingeschneit, Quartier teilen, Kutsche bricht zusammen |
| Ankunft mit Mission | Eine Figur bringt Auftrag/Befehl/Geschenk mit |
| Verfolgung / Captivity (B2) | Velmar/Halvara-Geometrie, Magie-Dämpfung, Verhör |

### 1.4 Drei Akt-Sets aus Register

Aus `buch/leseproben/36-anatomie-register-explizit.md` ziehe drei Set-Nummern, die einen narrativen Bogen bilden:

**Bogen-Logik:**
- Set 1 = Auftakt (sanft, Vorspiel-Niveau, Annäherung)
- Set 2 = Hauptakt (zentrale Penetration / zentrale Geste)
- Set 3 = Schluss-Akt + Aftercare-Beat (Cum, Cleanup, ineinander liegen)

**Heat-Bögen** (Alphina/Sorel oder Heat-Pärchen) — Beispiele:
- 4.19 Cunnilingus MF → 4.4 Glied in Vulva → 4.39 Creampie
- 4.21 Doggystyle → 4.45 Spiegel-Spiele → 4.39 Creampie
- 4.20 Edging → 4.5 Deepthroat → 4.41 Cum im Mund + Schluck

**BDSM-Bögen** (Vesper/Maren) — Beispiele:
- 4.30 Verschnürung → 4.99 Hook+Halsband → 4.123 Hard Take + Verbal
- 4.50 Réage-Ankleidungs-Ritual → 4.94 Long T&D → 4.118 Color-System
- 4.25 Halsband+Kette → 4.122 Choke-via-Chain → 4.40 Anus-Cum + Pfropfen
- 4.83 English Discipline → 4.91 Confession+Punishment → 4.86 Drei-Cum-Mandate

**Tantra-Bögen** (jedes Pärchen):
- 4.112 Wachstuch-Öl → 4.113 Slow Sex 60 min → 4.116 Full-Body-Kissing
- 4.114 Tantra-Schwanzmassage → 4.115 Tantra-Empfang → 4.113 Slow Sex

**Captivity-Bögen** (Varen + Sub-Figur in B2):
- 4.50 Réage-Ankleidung → 4.43 (Solo) als verordnetes Eigen-Ritual → 4.121 Wand-Loch + Anonyme Hands
- (Magie-Dämpfung Lederhalsband zwingend; siehe `10-magie-system.md` Z.80-99)

Bei Token `bdsm` / `heat` / `tantra` Bogen-Pool entsprechend filtern.

## Phase 2 — Story-Skelett

Drei Sektionen, Wortverteilung bei 1000 Wörter Ziel:

| Sektion | Wörter | Inhalt |
|---|---|---|
| **Setting** | ~250 | Ort etablieren über die Bezugsbrille einer der Figuren. Sinnesdetails (Geruch/Tastsinn/Geschmack/Temperatur/Textur — King-Niveau). Mundane Details die später feuern (Tschechow). Tageszeit, Wetter, Material des Raums. Die Figur bewegt sich, wartet, hört |
| **Begegnung** | ~350 | Auftakt-Akt (Set 1). Eintritt der zweiten Figur (oder Erinnerung an die erste, falls nicht da). Dialog knapp, Verb-zuerst-Befehl wo BDSM. Körperliche Annäherung, erste Berührung, Material des Kleides/Hauts |
| **Akt** | ~400 | Hauptakt (Set 2) → übergehend in Schluss-Akt (Set 3). Anatomie-Vokabular aus Register. Aftercare-Beat (zwei bis vier Sätze) als Schluss |

**Bei `kurz` (500 W)**: 125 / 175 / 200.
**Bei `lang` (1500 W)**: 375 / 525 / 600.

## Phase 3 — Stil-Anker

**Pflicht-Reads vor dem Schreiben** (Hauptsession):
- `buch/00-positioning.md` — Marktposition, Heat-Level-Kategorien
- `buch/01-autorin-stimme.md` — Begehren-Vokabular pro POV, Anti-Patterns, Erotik-Regeln
- `buch/02-stilregeln-v2.md` — harte Limits, Stakkato-Verbot, halb/nicht-sondern, Verb-Präzision
- `buch/leseproben/36-anatomie-register-explizit.md` — Anatomie-Vokabular und Variante-D-Vorlagen für die drei gewürfelten Sets
- POV-Dossier(s) der Hauptfigur(en): `buch/pov/<figur>.md` + ggf. `<figur>-schreibblatt.md`

**Inline-Cheat-Sheet** (nicht-verhandelbare Kernpunkte):

*Stil:*
- Réage primär für Vesper/Maren-BDSM. Yarros/Maas/Robert primär für Alphina/Sorel-Heat. Simone als Sekundärfor BDSM.
- Anus-Klarheits-Kette: erste Erwähnung klar (Anus / After / Hinterteil), Folge-Erwähnungen poetisch (Ring / Öffnung / Pforte / Lenden in V/M-Zone)
- *Lenden* in V/M-BDSM erlaubt (Réage-Standard), in A/S-Heat meiden (kitschig-Risiko)
- Mündlicher Lese-Test pro Satz — würde ein Mensch das so sagen, ohne zu stocken?
- Verb-Präzision: keine Default-Sein-Verben (lag/war/stand/saß) als Tic, keine Default-Aktionsverben (machen/gehen/legen/nehmen/halten/lassen)
- KEINE Stakkato-Ketten in Dialog/Erzähler — Pflicht-Prüfung pro Einsatz
- KEIN „nicht X, sondern Y" als Tic — Default streichen
- KEIN „halb X" außer kanonisch
- KEINE Sinnfreien Negationen
- KEINE Adverb-Tags / Denk-Tags („sie dachte")
- Emotionen nie benennen — Körper zeigen (Ausnahme: Selbsterkenntnis mit Körper-Marker)

*Welt-Canon:*
- KEINE Anglizismen, frühes 19. Jhd. Register
- KEINE realweltlichen Monatsnamen (Mai → Blütenmond)
- KEINE Tempel/Priester/Götter/Liturgie/Sakrament — areligiöser Gründungskanon
- KEINE Magie-Imperative wie Hund-Kommando — Magie via Wille+Vorstellung
- KEIN „Resonanz" in Prosa — Canon-Begriff, draußen
- KEINE Schemen-Benennung in Prosa
- KEINE Jacke/Bluse — Mantel/Hemd/Tunika/Rock/Westen
- Sorel hat keinen Bart — glatt rasiert
- Alphina-Heat-Echo: Pflanzen-Manifestation (Farne bei Sorel, Dornen mit Purpurblüten bei Varen, Glutmoos bei Runa)
- Alphina-Resonanz = Zellwachstum (Pflanzen+Mensch+Tier), faktisch unsterblich (nutzt es nicht)
- Maren Wasser-Resonanz: Steuern/Kochen/Vereisen/Hören, alles 30-60 Sek, nie instant
- Stein ist inert. Pflanzen wachsen DURCH den Stein. Quellen sind Stein-Art.
- Magie hat keine Kosten — kein Erschöpfungs-/Blut-/Limit-Beat
- Velmar-Halsband-Magie-Dämpfung Stufe 5+, matt-violett glühender Stahlring
- Talven: Blutmagie (Selbstlehre, exklusiv), KEINE „Resonanz-Ernte"
- Schemen sind lautlose Magie-Wesen, Schaden NUR durch aktiv ausgelöste Magie
- Zwei Monde in Moragh, einmondig in Thalassien
- Währung in Prosa „Münze" oder Stückzahl, NIE Solm/Stüber

*Anti-Klischee:*
- Sinnes-Details konkret (Material, Geruch, Tastsinn) — keine abstrakten Aphorismen
- Tonwert/Grauwert nur für Bilder/Atmosphäre, NICHT für Mensch-Gesicht (dort: bleicher, röter, Schatten)
- „Puls" durch Körperstelle ersetzen (Handgelenk, Halsschlagader, Kehle)
- Sorel in Nähe-Szenen riecht nach Haut/Leinen/Abendluft, NICHT Pyrogallol/Fixiersalz
- Alphina keine Uhrmacher-Präzision (keine Fingerknochen/Atemzüge/Sekunden zählen)
- Sub-Agency: Marens „Ich will." als aktive Zustimmung Réage-konform

## Phase 4 — Schreiben

Hauptsession schreibt selbst, sektionsweise:

1. **Setting-Block** — schreiben, dann inline-Selbstcheck (Stil-Limits, Welt-Canon, Verb-Präzision)
2. **Begegnungs-Block** — schreiben, Auftakt-Akt aus Register integrieren, Selbstcheck
3. **Akt-Block** — Hauptakt → Schluss-Akt → Aftercare, Variante-D-Vorlagen aus Register als Bauplan, Selbstcheck

Nach jedem Block kurz auf Wortzahl prüfen. Toleranz: ±15% auf Zielwert. Wenn ein Block deutlich zu lang/kurz wird, korrigieren bevor weitergeschrieben wird.

## Phase 5 — Output

Datei: `buch/kurzgeschichten/{YYYYMMDD}-{slug}.md`

`{YYYYMMDD}` = aktuelles Datum (heute aus `currentDate`-Frame oder `Get-Date -Format yyyyMMdd`).
`{slug}` = kurzer Kebab-Case-Titel aus den Hauptfiguren + Ort, max. 6 Wörter (z.B. `vesper-maren-werft-edging`, `alphina-sorel-atelier-creampie`).

**Frontmatter:**

```yaml
---
typ: Kurzgeschichte (Würfel-Output)
canon_status: Stil-Übung — kein Plot-Canon, keine Kaskade
gezogen_am: YYYY-MM-DD
figuren: [Name1, Name2, ...]
welt: Thalassien | Moragh
ort: ...
tageszeit: ...
monat: ...
witterung: ...
begegnungs_anlass: ...
akt_sets: [4.NN, 4.MM, 4.PP] aus 36-anatomie-register-explizit
heat_level: ... (z.B. „explizit Heat", „explizit BDSM", „tantra-slow")
laenge: ~1000 Wörter
---
```

**Body:**
- H1: Story-Titel (drei bis sechs Wörter, präzise, kein Klischee)
- Drei H2-Subheadings: `## Setting`, `## Begegnung`, `## Akt` (oder thematische Subheadings, falls die Story es trägt)
- Am Ende: H2 `## Würfel-Notiz` mit den exakten Würfel-Ergebnissen (Reproducibility-Anker)

## Phase 6 — Commit + Deploy

Nach dem Schreiben:

1. Wortzahl prüfen, melden
2. User fragen: „Committen und deployen?"
3. Wenn ja: `git add buch/kurzgeschichten/{datei}.md && git commit -m "feat(kurzgeschichten): {titel}"` → Hook deployt automatisch via Push

**Web-Output:** Beim Push läuft `generate-lesen.sh`, das `scripts/build-kurzgeschichten.py` aufruft. Das Skript rendert alle `buch/kurzgeschichten/*.md` zu `kurzgeschichten/index.html`, verfügbar unter `https://alphina.net/kurzgeschichten/`. Reduziertes Layout: nur Seitentitel + Liste der Geschichten (neueste zuerst), keine Sidebar, kein Filter. Jede Geschichte bekommt einen Anker `#kg-{datum}-{slug}`, Comment-System ist aktiv (analog Leseproben).

## Wiederholbarkeit

Wenn User die gleiche Konstellation noch einmal mit anderen Akt-Sets oder anderem Anlass will: aus `gezogen_am`-Frontmatter und Würfel-Notiz exakte Variante reproduzieren oder gezielt einen Würfelwert tauschen.

## Hinweise an die Schreibende-Hauptsession

- **Kein Subagent.** Du schreibst selbst. Stil ist zu sensibel für Auslagerung.
- **Lies die Pflicht-Reads.** Auch wenn die Story klein wirkt — Stilregeln und Welt-Canon liegen in Master-Files, nicht in deinem Kopf.
- **Würfel transparent.** Zeig dem User die Würfel-Ergebnisse vor dem Schreiben. Wenn die Konstellation Plot-konfliktet, sag es und schlag Würfel-Ersatz vor.
- **Kein Aphorismen-Theater.** Keine narratorischen Glossen, keine kryptischen Meta-Kommentare („Etwas in X, das nicht zu Y gehörte"). Subtext durch Körper, nicht durch Erzähler.
- **Ein Akt-Set ist ein Bauplan, kein Skript.** Variante-D aus dem Register zeigt die Bewegung — übernimm Anatomie-Vokabular und Material-Schritte, aber schreibe für *deine* Figuren in *deinem* Setting, nicht copy-paste.
- **Aftercare zählt mit.** Bei BDSM-Bögen ist der Schluss-Beat (zusammen liegen, sich halten, Wasser trinken, sich anschauen) Pflicht — drei bis sechs Sätze, keine Exposition.
