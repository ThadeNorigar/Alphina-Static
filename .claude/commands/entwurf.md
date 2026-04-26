# /entwurf — Phase 1: Plot-Entwurf als Fließprosa-Exposé

**Ziel:** Plot, Struktur, Logik, Charakter-Dynamik fuer ein Kapitel als Fließprosa-Exposé festklopfen. **Kein Prosa-Ton, kein Rhythmus, keine Stil-Arbeit.** Diese Phase macht den Plot belastbar, nicht die Sprache.

**Modell-Soll:** Sonnet (Hauptsession). Alle Subagenten explizit per Override.

## Input

`$ARGUMENTS` = Kapitel-ID im Format `B{N}-K{KK}` (z.B. `B1-K12`) oder `B{N}-I{N}` (Interludium).

Wenn kein Argument: frage welche Kapitel-ID.

## Phase 0: Guard-Checks

**Diese Pruefungen MUESSEN bestanden sein, bevor irgendwas geladen wird.**

### 0.1 Modell-Check

Wenn diese Session NICHT auf Sonnet laeuft (z.B. Opus oder Haiku):

> WARNUNG: Du bist auf [Modell]. Diese Phase ist auf Sonnet optimiert (Plot-Arbeit, keine Prosa). Auf Opus zahlst du den 5x-Aufpreis ohne Mehrwert. Empfehlung: Session beenden, neu starten mit `claude --model sonnet`. Trotzdem weiter? [Autor antwortet]

Bei Opus: warten auf explizites "weiter" oder "ja".
Bei Sonnet: stillschweigend weiter.

### 0.2 Parameter-Parsing

Parameter `B1-K12` parsen:
- `buch` = 1
- `typ` = K (Kapitel) oder I (Interludium)
- `nr` = 12

In `buch/status.json` unter `buch{N}.akte[*].kapitel` nachschlagen ob die ID existiert.

### 0.3 Status-Check

Aus `status.json` den `state` des Kapitels lesen.

| Aktueller Status | Verhalten |
|---|---|
| fehlt / `idee` | Normal weiter |
| `entwurf*` | Frage: "Kapitel ist schon in Phase X. Ueberschreiben oder weiterarbeiten?" |
| `ausarbeitung` / `lektorat` / `final` | HARTER ABBRUCH: "Kapitel ist schon weiter in der Pipeline. Rueckstufung erwuenscht? Dann erst Status manuell zuruecksetzen." |

### 0.4 Handoff-Check

Pruefen ob `buch/kapitel/B1-K12-handoff.md` existiert.

- Wenn ja: lesen, beruecksichtigen (z.B. wenn Autor nach Feedback zurueck in die Entwurfs-Phase gesprungen ist). Dem Autor zeigen: "Altes Handoff-File gefunden von Phase X. Verwenden oder loeschen?"
- Wenn nein: normal weitergehen.

## Phase 1: Kontext laden — schlank

**Schritt 1: Kontext-Extraktor ausfuehren (Bash):**

```bash
python scripts/kapitel-kontext.py {ID} --phase entwurf
```

Das Script liefert auf stdout (~3-4k Tokens): Kapitel-Info, Nachbar-Kapitel, Zeitleisten-Events bis hierher, offene Tschechow-Waffen, Aktplan-Snippet, **Empfohlene Leseproben** (Ton-Referenzen mit POV/Figuren-Score), **Vorgaenger-Kapitel mit Figuren-Ueberlappung** (letzte 2 Kapitel mit gemeinsamen Figuren, inkl. Pfadhinweis), Wissensstand der POV-Figur, Begegnungen, Wohnorte. **Diesen Output als Haupt-Kontext verwenden.**

**Schritt 2: Zusaetzlich mit Read laden (parallel):**

1. **`buch/00-positioning.md` ZUERST** (~800 W — Marktposition, Zielgruppe, Stilvektoren). Jede Plot-Entscheidung muss an diesem Positioning gemessen werden. Bei Konflikt mit anderen Docs gilt Positioning.
2. `buch/00-canon-kompakt.md` (~800 W — Welt/Figuren/Magie auf einen Blick)
3. `buch/pov/{figur}.md` — POV-Dossier der Ziel-Figur (POV aus dem Kontext-Output ablesen)
4. **Top-1 bis Top-2 der empfohlenen Leseproben volle lesen** (aus dem Abschnitt „Empfohlene Leseproben" des Extraktors, „Primaer"-Eintraege mit Score ≥10). Diese sind Ton-Referenz fuer diese Szene — nicht Plot-Vorlage. Die `B2/B3`-Proben nur dann lesen, wenn das Kapitel tatsaechlich in einem dunklen Register spielt.
5. **Die zwei Vorgaenger-Kapitel mit Figuren-Ueberlappung** (aus dem Abschnitt „Vorgaenger-Kapitel") — wenn das direkte Vorgaenger-Kapitel (K-1) dabei ist, **volle lesen** (Ton-Anschluss). Das zweite Vorgaenger-Kapitel reicht als Nachbar-Kurztext aus dem Extraktor; nur wenn eine direkte Referenz im aktuellen Kapitel vorkommt (Objekt, Geste, Figur-Motiv), volle lesen.

**NICHT laden:**
- `buch/zeitleiste.json` — NICHT MEHR DIREKT LADEN. Der Kontext-Extraktor liefert die relevanten Events (~3k statt ~36k Tokens)
- `buch/status.json` — NICHT MEHR DIREKT LADEN. Der Kontext-Extraktor liefert die relevanten Kapitel-Infos (~1k statt ~15k Tokens)
- `buch/00-welt.md` (zu gross, Inhalt steckt im Canon-Kompakt)
- `buch/10-magie-system.md` (dito)
- `buch/02-stilregeln-v2.md` (keine Stil-Arbeit in dieser Phase)
- `buch/kapitel/*.md` Volltexte (Inhalt steckt in den Summaries)
- Aktplaene komplett (Snippet steckt im Kontext-Output)
- `buch/kapitel-summaries.md` (Nachbar-Kapitel stecken im Kontext-Output)

**Ziel-Kontext: ~5-6k W.** Kontext-Extraktor (~3k) + Positioning (~800) + Canon-Kompakt (~800) + POV-Dossier (~500).

## Phase 2: Entwurf schreiben

Datei: `buch/kapitel/{ID}-entwurf.md` (mit Prefix, z.B. `B1-K12-entwurf.md`).

**Format strikt einhalten:**

```markdown
# {ID} — {Figur} — Entwurf

**POV:** {Figur} (3. Person nah, Praeteritum)
**Timeline:** {Monat/Jahreszeit, Anker zu vorherigem Kapitel}
**Wortziel Ausarbeitung:** 4.000-4.500 W
**Gaensehaut-Moment:** {Was physisch Unmoegliches passiert}

**Ton-Referenz-Leseproben (fuer /ausarbeitung):**
- `buch/leseproben/{XX}-{name}.md` — {Begruendung in einem Satz: warum diese Probe fuer dieses Kapitel passt}
- {1-3 Eintraege total. Aus dem Kontext-Extraktor-Output "Empfohlene Leseproben" auswaehlen.}

**Council-Leserinnen fuer /ausarbeitung:**
- {LINA / NORA / MEIKE / VICTORIA / KAYA} — {Begruendung in einem Satz: warum diese Stimme fuer dieses Kapitel relevant ist}
- {2-3 Eintraege total. Stimmen, die nicht passen, NICHT aufnehmen — keine Vollstaendigkeit erzwingen.}

## Szene 1 — {Titel/Ort}

**Wortziel:** 1.200-1.600 W (spaeter in Ausarbeitung)

{150-300 W Fließprosa-Exposé. Wer ist im Raum, wo ist der Raum,
 was passiert, welche Bewegung, welche Sinneseindruecke sind dominant,
 wohin geht der Beat am Ende. KEIN Dialog ausformuliert. KEIN Stil.}

**Dialog-Informationen:**
- {Figur A} erfaehrt: {Info 1, Info 2}
- {Figur B} erfaehrt: {Info 1}
- {Figur A}'s Erkenntnis am Ende: {innere Wendung}
- {Figur B}'s Erkenntnis am Ende: {innere Wendung}

**Tschechow-Waffen geladen:** {konkrete Gegenstaende/Details die spaeter zuenden}
**Tschechow-Waffen abgefeuert:** {was aus frueheren Kapiteln hier zuendet, oder "—"}
**Cross-POV-Ankerpunkte:** {Was muss konsistent sein mit Kap X}

## Szene 2 — ...
## Szene 3 — ...

## Kontinuitaets-Notizen
- Was weiß die POV-Figur am Anfang?
- Was weiß sie am Ende?
- Welches Wissen darf sie NICHT haben (Sorel-Prinzip)?
```

**Anforderungen an den Entwurf:**
- 2-4 Szenen (typisch 3)
- Jede Szene: Fließprosa-Exposé + Dialog-Info-Liste + Tschechow-Beats + Cross-POV
- KEIN ausformulierter Dialog (kein "..., sagte sie")
- KEINE rhetorischen Stilfiguren
- KEINE Sinnes-Schmuckwoerter (wir machen nur den Plot, nicht die Atmosphaere)
- Jeder Plot-Beat MUSS in den Dialog-Info-Listen oder im Fließprosa-Exposé stehen
- Gaensehaut-Moment ist Pflicht
- **Ton-Referenz-Leseproben** und **Council-Leserinnen** im Header gesetzt (siehe unten)

**Auswahl der Ton-Referenz-Leseproben (1-3 Stueck):**

Aus dem Kontext-Extraktor-Output „Empfohlene Leseproben" die fuer dieses Kapitel relevantesten waehlen. Auswahlkriterien:
- POV-/Figuren-Match (Alphina-Solo? Alphina/Sorel? Vesper/Maren? Gruppe?)
- Heat-Level / Register (commercial Heat? Schock + Gewalt? BDSM? Slow-Burn-Tension?)
- Strukturparallele (Kippmoment? Gruppenszene? Solo-POV? Konfrontation?)

Begruendung in einem Satz pro Probe — knapp, konkret, ohne Phrasen.

**Auswahl der Council-Leserinnen (2-3 Stueck):**

Aus den fuenf Archetypen aus `.claude/commands/book-council.md`:

| Stimme | Regal | Wann waehlen |
|--------|-------|--------------|
| **LINA** | Yarros, Maas, Rampling, Robert | Slow-Burn-Tension, Heat, commercial Romantasy, Alphina/Sorel-Naehe |
| **NORA** | Robert, Kennedy, Simone | Power-Dynamik, Schaerfe, Reibung, morally grey, Alphina/Varen, Konfrontation |
| **MEIKE** | Bardugo, Black, Kuang | POV-Disziplin, benannte Einzeldetails, Welt mit Zaehnen, Atmosphaere mit Bewegung |
| **VICTORIA** | Reage, Reisz, Rampling | BDSM-Szenen Vesper/Maren, Power-Exchange mit Grund, Material-Praezision |
| **KAYA** | Kuang, SenLinYu, Pierce Brown | Koerper unter Druck, Gewalt mit Folge, Trauma-Koerper, Schock, Tod |

Wahl: nur die 2-3 Stimmen, deren Erwartungs-Raster fuer dieses Kapitel passt. Stimmen, die nicht passen, weglassen — keine Vollstaendigkeit erzwingen. Begruendung in einem Satz pro Stimme.

**Beispiel K29 (Sorel allein im Lichthaus, Schemen-Schock, Dark Fantasy):**
- MEIKE — Solo-POV-Disziplin, benannte Einzeldetails, Schemen als Welt-mit-Zaehnen-Beat
- KAYA — Schock-Moment ohne Sanitisierung, Koerper unter Druck

**Was NICHT in dieser Phase festlegen:** Stilfeinheiten, Wortwahl, Satzlaenge, Heat-Pacing — das ist Ausarbeitung. Hier nur: welche Toene und welche Leserinnen passen zum Plot dieses Kapitels.

## Phase 3: Status setzen + Deploy

```bash
# status.json updaten via Edit oder kleinem Skript:
# - state: "entwurf"
# - entwurfs_datei: "B1-K12-entwurf.md"
git add buch/status.json buch/kapitel/{ID}-entwurf.md
git commit -m "feat({ID}): Entwurf — {Figur}"
git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull && bash generate-lesen.sh"
```

Status: `entwurf`. Autor kann den Entwurf jetzt online lesen.

## Phase 4: Schlanker Logik-Check (Subagent, sonnet)

Dispatch ueber Agent-Tool mit:
- `subagent_type: "general-purpose"`
- `model: "sonnet"`
- Prompt:

```
Du pruefst einen Kapitel-Entwurf von "Der Riss" auf Logik. Brutal.

Lies parallel:
1. buch/kapitel/{ID}-entwurf.md (der Entwurf)
2. buch/00-canon-kompakt.md (Welt/Figuren-Fakten)
3. buch/kapitel-summaries.md (was bisher geschah)

Pruefe:
- POV-Wissen: Weiß die Figur was sie weiß? Sorel-Prinzip bei JEDEM Eigennamen.
- Timeline-Sync: Monat/Jahreszeit konsistent mit den Summaries der vorherigen Kapitel?
- Magie-Regeln: Stimmen sie mit dem Canon-Kompakt?
- Anachronismen: Frühes 19. Jhd in Thalassien, Mittelalter+Magie in Moragh.
- Cross-POV-Dopplung: Sind Beats schon in einem anderen Kapitel beschrieben worden?
- Gaensehaut-Moment vorhanden?
- Premature Doubt: Zweifelt die Figur bevor das ausloesende Ereignis passiert?

Output: kurzer Bericht (max 1k Token), Findings als Tabelle (Szene, Typ, Problem, Fix).

Verdikt am Ende: BESTANDEN / NICHT BESTANDEN.
```

## Phase 5: Entwurfs-Council (2 Subagenten, sequenziell, sonnet)

### Subagent 1: Strukturanalyst

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "sonnet"`
- Prompt:

```
Du bist Strukturanalyst fuer "Der Riss" (Dark Romantasy, Buch 1).

Lies parallel:
1. buch/kapitel/{ID}-entwurf.md
2. buch/00-canon-kompakt.md
3. buch/pov/{figur}.md
4. buch/kapitel-summaries.md
5. Aus dem Aktplan den Abschnitt fuer Kapitel {nr}

Pruefe:
- Plot-Logik: Trifft jeder Beat? Gibt es Luecken in der Kausalkette?
- Tschechow-Oekonomie: Sind die geladenen Waffen sinnvoll? Werden frueher geladene Waffen hier abgefeuert?
- Aktplan-Match: Stimmt der Entwurf mit dem Aktplan ueberein? Wenn nicht, ist die Abweichung begruendet?
- Beat-Dichte: 2-4 Szenen, jede mit klarem Wendepunkt?
- Kontinuitaet: Passt das Kapitel zu den Summaries der vorherigen Kapitel? Sind Cross-POV-Ankerpunkte gesetzt?

Max 1k Token Output. Verdikt: BESTANDEN / NICHT BESTANDEN + 3-5 konkrete Findings.
```

### Subagent 2: Beziehungs-Lektorin

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "sonnet"`
- Prompt:

```
Du bist Beziehungs-Lektorin fuer "Der Riss" (Dark Romance, BDSM, Romantasy).

Lies parallel:
1. buch/kapitel/{ID}-entwurf.md
2. buch/00-canon-kompakt.md
3. buch/pov/{figur}.md
4. buch/kapitel-summaries.md

Pruefe:
- Charakter-Arc: Hat die POV-Figur eine Wendung im Kapitel? Was lernt/verliert sie?
- Power-Dynamik: Wo zeigt sich Macht/Hingabe? Bei BDSM-Szenen: ist es Beziehungsarbeit, nicht Dekoration?
- Begehren als Unterstrom: Auch ohne Sexszene — wo brennt es zwischen den Figuren? Blicke, Naehe, Vermeidung?
- Emotionale Bogenfuehrung: Steigt die emotionale Spannung? Gibt es eine Bruchstelle?
- Beziehungs-Status: Veraendert sich das Verhaeltnis zwischen den Figuren in diesem Kapitel?

Aus Beat-Strukturen kann man manches NICHT sehen (Prosa-Ton, Sprach-Erotik). Das ist OK — fokussier dich auf das was im Entwurf erkennbar ist.

Max 1k Token Output. Verdikt: BESTANDEN / NICHT BESTANDEN + 3-5 konkrete Findings.
```

## Phase 5b: Council-Leserinnen-Review (2-3 Subagenten parallel, sonnet)

**Zweck:** Die im Entwurfs-Header festgelegten Council-Leserinnen lesen den Entwurf in-character und bewerten kritisch, ob der **Plot** fuer ihren Genre-Erwartungs-Raster taugt. Pro Stimme: Verdict + Score + Findings. Gate: **≥90% Durchschnitt** = bestanden.

**Wichtig:** Diese Phase pruefen den **Plot** des Entwurfs, NICHT die Prosa (es gibt noch keine). Die Stimmen urteilen ueber Plot-Beats, Beat-Dichte, Power-Dynamik, Schock-Wirkung, Genre-Tauglichkeit, Cliffhanger-Bewegung — alles auf Beat-Ebene.

Aus dem Entwurfs-Header Feld „Council-Leserinnen fuer /ausarbeitung" die 2-3 festgelegten Stimmen entnehmen. Pro Stimme einen Subagenten dispatchen:

- `subagent_type: "general-purpose"`
- `model: "sonnet"`
- Prompt-Template (pro Stimme angepasst):

```
Du bist {STIMME-NAME} aus dem book-council von "Der Riss".

Lies dein Profil zuerst:
- .claude/commands/book-council.md (Abschnitt "Die fuenf Stimmen", deine Stimme)

Verinnerliche: Regal, Erwartungs-Raster, Schaltet-ab-bei, Persoenlichkeit. Du bist diese Leserin, kein neutraler Kritiker.

Dann lies:
- buch/kapitel/{ID}-entwurf.md (der Entwurf — Plot, Beats, Dialog-Infos, Tschechow, KEINE Prosa)
- buch/00-positioning.md Abschnitt 9 (95%-Gate, vier Pflichten)

Deine Aufgabe: Bewerte den **Plot dieses Entwurfs** aus deinem Genre-Erwartungs-Raster.

Pruefe:
- Trifft der Plot dein Genre? (z.B. LINA: ist Slow-Burn-Tension da? NORA: ist Schaerfe da? KAYA: hat die Gewalt eine Folge?)
- Sind die Beats stark genug fuer dich? Wo flacht es ab? Wo zieht es?
- Gaensehaut-Moment: trifft er fuer dich? Funktioniert er in deinem Register?
- Power-/Beziehungs-Dynamik (wenn relevant): erfuellt sie deine Erwartungen?
- Cliffhanger-/Beat-Bewegung: wuerdest du im naechsten Kapitel weiterlesen?
- Wuerde dieser Entwurf, wenn er sauber ausgearbeitet wird, dich als Leserin zufrieden stellen?

Sei in-character: streng, direkt, keine Hoeflichkeit, in deiner Sprache. Zitiere wenn moeglich aus dem Entwurf.

Output:
- 3-5 Saetze Verdict in-character (deine Stimme, dein Ton)
- Commercial-Score 0-100% fuer den Plot dieses Entwurfs aus deiner Sicht
- 3-5 konkrete Findings: was muss vor /ausarbeitung verbessert werden? Konkret, Beat-genau.

Max 1k Token.
```

Alle 2-3 Subagenten parallel dispatchen (sie sind unabhaengig).

## Phase 6: Konsolidierter Bericht

Zeige dem Autor:

1. **Logik-Check Findings** (Tabelle, knapp)
2. **Strukturanalyst** Findings + Verdikt
3. **Beziehungs-Lektorin** Findings + Verdikt
4. **Council-Leserinnen** (2-3 Stimmen):
   - Pro Stimme: Verdict (1-2 Saetze, in-character) + Score
   - **Durchschnitts-Score** der festgelegten Stimmen
   - Niedrigste Stimme als Risiko-Signal
5. **Gesamt-Verdikt** mit Leserinnen-Gate:

| Durchschnitt Leserinnen-Score | Verdikt |
|-------------------------------|---------|
| **≥ 90 %** | **PLOT-COUNCIL BESTANDEN.** Freigabe-Kandidat. |
| **80–89 %** | **GRENZWERTIG.** Findings einarbeiten, dann Re-Review oder Autor-Entscheidung. |
| **70–79 %** | **NACHBESSERN.** Plot-Lücken in den Findings — vor `entwurf-checked` einarbeiten. |
| **< 70 %** | **DURCHGEFALLEN.** Plot trifft das Genre-Profil nicht. Zurueck zu Phase 2, Beats neu denken. |

Frage: „Findings einarbeiten, oder ist der Plot so OK?"

Bei OK + Score ≥ 90 % → Status `entwurf-checked` + Deploy.
Bei OK + Score 80–89 % → Autor bestaetigt explizit „trotzdem ok" → `entwurf-checked` + Deploy mit Notiz.
Bei < 80 % → kein `entwurf-checked` ohne explizite Autor-Override.

## Phase 7: Feedback-Loop

Innerhalb derselben Session:
- Fixes einarbeiten direkt im Entwurf (Edit-Tool bevorzugt)
- Re-deploy (Status bleibt `entwurf-checked`)
- Warten auf naechstes Feedback

Bei Token-Druck (Session wird voll):
> Session wird voll. Soll ich ein Handoff-File schreiben und wir machen mit `/entwurf {ID}` in einer frischen Session weiter?

## Phase 8: Autor-Freigabe ("entwurf ok")

Wenn der Autor explizit *"entwurf ok"* / *"plot freigegeben"* sagt:

### 8.1 Status setzen
- `state: "entwurf-ok"` in status.json
- Deploy

### 8.2 Handoff-File generieren (Subagent, haiku)

Dispatch:
- `subagent_type: "general-purpose"`
- `model: "haiku"`
- Prompt:

```
Du erstellst ein Handoff-File fuer den Phasen-Uebergang von /entwurf zu /ausarbeitung.

Datei: buch/kapitel/{ID}-handoff.md

Lies kurz: buch/kapitel/{ID}-entwurf.md (nur Header und Szenen-Titel, nicht die ganzen Beats).

Schreibe das Handoff im folgenden Format:

# Handoff — {ID}

**Von Phase:** entwurf → **Zu Phase:** ausarbeitung
**Erstellt:** {aktuelles Datum/Uhrzeit}
**Status beim Handoff:** entwurf-ok

## Modell-Empfehlung
claude --model opus

## Aufruf fuer naechste Session
/ausarbeitung {ID}

## Kontext fuer naechste Session
- POV: {Figur aus Entwurfs-Header}
- Wortziel: 4.000-4.500
- Timeline-Anker: {aus Entwurfs-Header}
- Freigegebener Entwurf: buch/kapitel/{ID}-entwurf.md
- Ton-Referenz: buch/kapitel/{letztes-fertiges-kapitel-gleichen-povs}.md

## Anweisungen
- Prosa aus dem Entwurf ausarbeiten, Plot nicht veraendern
- Jeder Dialog-Info-Punkt aus dem Entwurf muss in der Prosa landen
- Keine Plot-Aenderung ohne Rueckkehr zu /entwurf

Max 100 Wörter Bericht zurueck.
```

### 8.3 Harter Stop

Zeige dem Autor:

> ENTWURF FREIGEGEBEN. Status: entwurf-ok.
>
> Naechster Schritt: NEUE SESSION mit Opus.
>
> 1. Diese Session beenden (Ctrl+C oder /exit)
> 2. Neue Session starten: `claude --model opus`
> 3. Im neuen Terminal: `/ausarbeitung {ID}`
>
> Das Handoff-File `buch/kapitel/{ID}-handoff.md` wird automatisch von der naechsten Session gelesen.
>
> Diese Session schreibt jetzt nichts mehr. Bitte beende sie.

**WICHTIG:** Nach diesem Stop NICHT weiterarbeiten, auch wenn der Autor noch Fragen stellt. Auf weitere Fragen antworten mit: "Ich darf in dieser Phase nicht mehr in das Kapitel eingreifen. Bitte starte die /ausarbeitung-Session."

## Gates (Zusammenfassung)

| Gate | Bedingung |
|---|---|
| Logik-Check | Bestanden oder vom Autor bewusst akzeptiert vor `entwurf-checked` |
| 2 Council-Agenten (Strukturanalyst + Beziehungs-Lektorin) | Beide bestanden oder bewusst akzeptiert vor `entwurf-checked` |
| **Council-Leserinnen (2-3, Phase 5b)** | **Durchschnitts-Score ≥ 90 %** fuer `entwurf-checked` ohne Override. 80–89 % = Autor-Override moeglich. < 80 % = nachbessern Pflicht. |
| Autor-Freigabe | Pflicht fuer `entwurf-ok`. Ohne diese kein Phase-Wechsel. |

## Regeln

- Lade NUR die Files aus Phase 1. Kein "schnell mal die Weltbibel checken".
- Schreibe KEINE Prosa. Nur Beats, Info-Listen, Strukturen.
- Setze NIEMALS `entwurf-ok` ohne explizites OK des Autors.
- Bei Konflikten zwischen Aktplan und zeitleiste.json gewinnt zeitleiste.json.
- Schreib Umlaute aus (ä, ö, ü, ß). KEIN ae/oe/ue.
- Deutsch.

$ARGUMENTS
