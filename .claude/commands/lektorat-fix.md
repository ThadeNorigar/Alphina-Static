# /lektorat-fix — Phase 3: Lektorats-Fixes (Token-sparend)

**Ziel:** Kleinere textuelle Aenderungen am Kapitel nach Lektorats-Feedback des Autors. **Token-sparsamst.** Kein Neuschreiben, kein Plot-Anfassen, keine Stil-Pruefungen, kein Council.

**Modell-Soll:** Sonnet (Default) oder Haiku (fuer Mikro-Fixes).

## Input

`$ARGUMENTS` = Kapitel-ID im Format `B{N}-K{KK}` (z.B. `B1-K12`).

Wenn kein Argument: frage welche Kapitel-ID.

## Phase 0: Guard-Checks (HART)

### 0.1 Modell-Hinweis (kein Abbruch)

Wenn diese Session auf Opus laeuft:

> HINWEIS: Du bist auf Opus. Fuer Lektorat-Fixes reicht Sonnet oder Haiku. Opus ist hier teuer ohne Mehrwert.
>
> Empfehlung: Session beenden, neu starten mit `claude --model sonnet` oder `claude --model haiku`.
>
> Trotzdem auf Opus weiter? [Autor antwortet]

Kein harter Abbruch — Autor entscheidet.

### 0.2 Handoff-Check (ZWINGEND)

Pruefen ob `buch/kapitel/{ID}-handoff.md` existiert.

- Wenn JA: lesen, Phase-Markierung pruefen ("Von Phase: ausarbeitung → Zu Phase: lektorat-fix").
  - Wenn passt: weiter.
  - Wenn nicht: HARTER ABBRUCH. *"Falsches Handoff-File. Phase-Markierung ist X, erwartet ist lektorat-fix. Bitte korrigieren oder Status pruefen."*
- Wenn NEIN: HARTER ABBRUCH:
  > Kein Handoff-File gefunden. Diese Phase kann nur nach abgeschlossener /ausarbeitung starten.
  >
  > Pruefe den Status mit `/status {ID}` oder fuehre erst /entwurf und /ausarbeitung durch.

### 0.3 Status-Check

Aus `status.json` den Status lesen.

| Aktueller Status | Verhalten |
|---|---|
| `lektorat` | Normal weiter |
| `final` | WARNUNG: "Kapitel ist schon final. Wirklich zurueck ins Lektorat? Bestaetigen." |
| alles frueher | HARTER ABBRUCH: "Kapitel ist nicht im Lektorat. Erst /ausarbeitung abschliessen." |

### 0.4 Parameter-Parsing

Parameter `B1-K12` parsen, in `status.json` nachschlagen, `datei`-Feld lesen.

## Phase 1: Kontext laden — Minimum

**NUR diese Files, parallel mit Read:**

1. `buch/kapitel/{datei aus status.json}` — das zu fixende Kapitel
2. `buch/02-stilregeln-v2.md` — fuer Referenz, FALLS der Autor eine Regel anspricht (sonst nicht aktiv nutzen)

**NICHTS ANDERES.** Kein Canon-Kompakt, keine POV-Dossiers, keine Summaries, keine Zeitleiste, kein vorheriges Kapitel, keine Aktplaene.

**Falls der Autor eine Fakten-Frage hat** (z.B. "War Maren schon im Archiv?"): `python scripts/kapitel-kontext.py {ID} --phase lektorat` liefert Nachbar-Kapitel-Kontext (~400 Tokens). Nur bei Bedarf ausfuehren, nicht standardmaessig.

**Ziel-Kontext: ~5-8k W.** Primaer das Kapitel selbst.

**Begruendung:** Lektorats-Fixes sind chirurgisch. Wenn der Autor sagt *"Seite 3, zweiter Absatz, der Satz klingt schief"* braucht Claude nur den Satz im Kontext. Wenn er sagt *"die Szene im Lagerhaus fuehlt sich zu hastig an"* braucht Claude die Szene — aber nicht die halbe Weltbibel.

## Phase 2: Arbeitsmodus — Autor-getrieben

### Vorgehen pro Fix-Runde

1. Der Autor gibt Rueckmeldung. Konkret. Bevorzugt mit Zitat, Zeilennummer oder Szenen-Verweis.
2. Claude liest die betroffene Stelle (falls noch nicht im Kontext).
3. Claude schlaegt eine Aenderung vor ODER fuehrt sie direkt durch (je nach Klarheit der Rueckmeldung).
4. Claude wendet die Aenderung mit dem **Edit-Tool** an (NICHT Write — das frisst Tokens).
5. Knapp bestaetigen: *"Zeile 142 angepasst, Absatz 18 gestrichen."*

### Harte Regeln

- **Edit-Tool bevorzugt vor Write-Tool.** Jeder Write eines grossen Files verschwendet Tokens. Edit mit praeziser old/new-String ist billiger.
- **Kein ungefragtes Umformulieren.** Claude macht NUR was angefragt wurde.
- **Auffaellige Stellen flaggen, nicht fixen.** Wenn beim Bearbeiten andere Stellen auffallen: *"Mir faellt auf Seite 7 noch X auf — willst du das auch angehen?"* — aber nicht selbststaendig aendern.
- **Keine Stil-Pruefung ohne Auftrag.** Kein neuer Stil-Check, kein Council, keine Wort-Zaehlung. Die Phase ist bewusst ungeprueft, weil die Arbeit punktuell ist und Pruefungen Kontext fressen.
- **Keine Reformulierungen "weil es klingt besser".** Nur Aenderungen die der Autor angefragt hat.

## Phase 3: Deploy nach jeder Fix-Runde

```bash
git add buch/kapitel/{datei}
git commit -m "fix({ID}): Lektorat — {kurze Beschreibung}"
git push
ssh adrian@adrianphilipp.de "cd ~/apps/Alphina-Static && git pull && bash generate-lesen.sh"
```

Status bleibt `lektorat`. Autor kann sofort online die geaenderte Stelle lesen.

## Phase 4: Feedback-Loop

Session bleibt offen fuer mehrere Fix-Runden. Der Kontext waechst nur langsam, weil jede Runde nur ein kleines Diff ist.

Wenn die Session doch zu voll wird (z.B. nach 10+ Runden):
- Handoff-File aktualisieren mit "bisher bearbeitet: ..." Liste
- Session-Break vorschlagen: *"Session wird voll. Frische Session mit /lektorat-fix {ID} weitermachen?"*

## Phase 5: Autor-Freigabe fuer `final`

**Claude darf den Status NIEMALS eigenmaechtig auf `final` setzen.**

Nur wenn der Autor explizit *"lektorat ok"* / *"final setzen"* / *"jetzt final"* sagt:

1. `state: "final"` in status.json
2. commit: `chore({ID}): Status final — Lektorat abgeschlossen`
3. push + deploy
4. **Handoff-File loeschen:** `rm buch/kapitel/{ID}-handoff.md`
5. Bestaetigung an Autor: *"Status final gesetzt. Handoff-File entfernt. Kapitel abgeschlossen."*
6. Hinweis: *"Nicht vergessen: kapitel-summaries.md fuer {ID} ergaenzen, damit zukuenftige /entwurf-Sessions Bescheid wissen."*
7. Optional: anbieten den Summary-Eintrag direkt zu schreiben (das ist eine kleine Aufgabe und passt noch in die Session).

## Phase 6: Session-Ende

Keine neue Session erzwungen. Die Lektorats-Session kann einfach geschlossen werden. Wenn final gesetzt: kein Handoff mehr (die Pipeline endet hier).

## Sonderfall: Grosse Aenderungen gewuenscht

Wenn der Autor schreibt *"die ganze Szene 2 nochmal"* oder *"das gesamte Kapitel klingt zu kalt, schreib es um"*:

> Das ist keine Fix-Arbeit mehr. Das ist Ausarbeitung. Vorschlaege:
>
> a) Status zurueck auf `entwurf-ok` oder `ausarbeitung`, neue /ausarbeitung-Session mit Opus
> b) Wenn nur Plot-Aenderung: zurueck auf `entwurf`, neue /entwurf-Session
>
> Welche Variante?

**Niemals grosse Umbauten in /lektorat-fix machen.** Das gehoert in Phase 2 mit Opus.

## Sonderfall: Plot-Problem entdeckt

Wenn beim Lesen ein echtes Plot-Problem auffaellt (z.B. Kontinuitaetsbruch zu einem anderen Kapitel):

1. Dem Autor das Problem zeigen
2. Vorschlagen: Rueckstufung auf `entwurf-ok` und neue /ausarbeitung
3. Niemals still im Lektorat den Plot anpassen

## Regeln

- Lade NUR die Files aus Phase 1.
- Edit-Tool > Write-Tool.
- Nichts anfassen was der Autor nicht angefragt hat.
- Setze `final` NUR auf explizites OK des Autors.
- Bei `final`: Handoff-File loeschen.
- Schreib Umlaute aus (ä, ö, ü, ß). KEIN ae/oe/ue.
- Deutsch.

$ARGUMENTS
